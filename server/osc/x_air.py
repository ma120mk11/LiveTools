import asyncio
from ipaddress import IPv4Address
import logging
import time
import threading
import socket
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder
from .osc import OSCBase
from .osc_server import server

logger = logging.getLogger(__name__)

class XairOSC(OSCBase):
    """
    Behringer X-Air specific OSC
    """
    state = 0

    def __init__(self):
        super().__init__()


    # def _init_heartbeat(self):
    #     self.send_osc_msg(self._set_surface, 8)

    async def connect(self, ip: IPv4Address, port: int):
        await super().connect(ip, port)
        # self.send_osc_msg("/xremote")
        # server.add_heartbeat("/heartbeat", 3, self.connection_change_handler, self._device_id)
        # self._init_heartbeat()

    def toogle_mute(self):
        self.send_osc_msg("/lr/mix/on", self.state)
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1

    def set_fx_mutes(self, conf):
        fx_status = [0, 0, 0, 0]
        if (conf['fx1']):
            fx_status[0] = int(conf['fx1'].get('enabled'))
        if (conf['fx2']):
            fx_status[1] = int(conf['fx2'].get('enabled'))
        if (conf['fx3']):
            fx_status[2] = int(conf['fx3'].get('enabled'))
        if (conf['fx4']):
            fx_status[3] = int(conf['fx4'].get('enabled'))
        
        self.send_osc_msg("/rtn/1/mix/on", fx_status[0])
        self.send_osc_msg("/rtn/2/mix/on", fx_status[1])
        self.send_osc_msg("/rtn/3/mix/on", fx_status[2])
        self.send_osc_msg("/rtn/4/mix/on", fx_status[3])

    def mute_all_fx(self):
        for i in range(1,5):
            self.send_osc_msg("/rtn/{}/mix/on".format(i), 0)

    # async def connection_change_handler(self, *args, **kwargs):
    #     """
    #     Callback method to be called when a connection change is noted.
    #     ``kwargs: connected: bool``
    #     """
    #     if kwargs.get('connected'):
    #         logger.info("%s re-connected", self._name)
    #         self._init_heartbeat()
    #         await self.set_status(self._CONNECTED)
    #     else:
    #         logger.error("%s disconnected", self._name)
    #         await self.set_status(self._NO_HEARTBEAT)
    #         asyncio.create_task(self._connection_retry())

    # async def _connection_retry(self):
    #     """
    #     Automaticly try to re-connect
    #     """
    #     while self.status != self._CONNECTED and self._enabled:
    #         self._init_heartbeat()
    #         await asyncio.sleep(5)

    # async def test_connection(self) -> bool:
    #     """
    #     Ardour uses a heartbeat instead of test
    #     """
    #     return True

    def find_mixer():
        print('Searching for mixer...')
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        client.settimeout(15)
        client.sendto("/xinfo\0\0".encode(), ("<broadcast>", XAirClient.XAIR_PORT))
        try:
            response = OscMessage(client.recv(512))
            # print(response.params)
        except socket.timeout:
            print('No server found')
            return None
        client.close()

        if response.address != '/xinfo':
            print('Unknown response')
            return None
        else:
            print('Found ' + response.params[1] + ' ('+response.params[2] + ')' + ' with firmware ' + response.params[3] + ' on IP ' + response.params[0])
            return response.params[0]


class OSCClientServer(BlockingOSCUDPServer):
    def __init__(self, address, dispatcher):
        super().__init__(('', 0), dispatcher)
        self.xr_address = address

    def send_message(self, address, value):
        builder = OscMessageBuilder(address = address)
        if value is None:
            values = []
        elif isinstance(value, list):
            values = value
        else:
            values = [value]
        for val in values:
            builder.add_arg(val)
        msg = builder.build()
        self.socket.sendto(msg.dgram, self.xr_address)


class XAirClient:
    """
    Handles the communication with the X-Air mixer via the OSC protocol
    """
    _CONNECT_TIMEOUT = 0.5
    _WAIT_TIME = 0.02
    _REFRESH_TIMEOUT = 5

    XAIR_PORT = 10024

    info_response = []
    
    def __init__(self, address, state):
        print("Init")
        self.state = state
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.msg_handler)
        self.server = OSCClientServer((address, self.XAIR_PORT), dispatcher)
        worker = threading.Thread(target = self.run_server)
        worker.daemon = True
        worker.start()
    
    def validate_connection(self):
        print("Validating connection")
        self.send('/xinfo')
        time.sleep(self._CONNECT_TIMEOUT)
        if len(self.info_response) > 0:
            print('Successfully connected to %s with firmware %s at %s.' % (self.info_response[2], 
                    self.info_response[3], self.info_response[0]))
        else:
            print('Error: Failed to setup OSC connection to mixer. Please check for correct ip address.')
            exit()
        
    def run_server(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.shutdown()
            exit()
        
    def msg_handler(self, addr, *data):
        # print 'OSCReceived("%s", %s, %s)' % (addr, tags, data)
        print('OSCReceived("%s", %s)' % (addr, data))
        if addr.endswith('/fader') or addr.endswith('/on') or addr.endswith('/level') or addr.startswith('/config/mute') or addr.startswith('/fx/'):
            self.state.received_osc(addr, data[0])
        elif addr == '/xinfo':
            self.info_response = data[:]
    
    def refresh_connection(self):
        # Tells mixer to send changes in state that have not been recieved from this OSC Client
        #   /xremote        - all parameter changes are broadcast to all active clients (Max 4)
        #   /xremotefnb     - No Feed Back. Parameter changes are only sent to the active clients which didn't initiate the change
        try:
            while True:
                self.server.send_message("/xremotenfb", None)
                time.sleep(self._REFRESH_TIMEOUT)
        except KeyboardInterrupt:
            exit()
            
    def send(self, address, param = None):
        self.server.send_message(address, param)
            


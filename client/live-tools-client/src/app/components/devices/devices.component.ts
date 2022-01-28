import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { IDevice, WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { ConfigureDeviceComponent } from './configure-device/configure-device.component';


// export class IDevice {
//   name: string;
//   description: string;
//   status: string;
//   ip: string;
//   port: number;
//   img: string;
//   is_loading: boolean;
//   is_enabled: boolean;
// }

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.sass']
})
export class DevicesComponent implements OnInit {
  is_loading = false;


  constructor(public ws: WebSocketService, private dialog: MatDialog) { }

  ngOnInit(): void {
  }

  onConfigure(device: IDevice) {
    const dialogRef = this.dialog.open(ConfigureDeviceComponent, {
      data: device
    })
  }

  getConnectionIcon(status: string){
    let icon: string = ""
    switch (status) {
      case "connected":
        icon = "check_circle"
        break;
      case "disconnected":
        icon = "error"
        break;
      default:
        icon = "warning"
        break;
    }
    return icon
  }


  getConnectionColour(status: string) {
    let colour: string = ""

    switch (status) {
      case "connected":
        colour = "green"
        break;
      case "disconnected":
        colour = "red"
        break;
      default:
        colour = "orange"
        break;
    }
    return colour
  }

}

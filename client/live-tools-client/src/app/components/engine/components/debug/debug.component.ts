import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';

@Component({
  selector: 'app-debug',
  templateUrl: './debug.component.html',
  styleUrls: ['./debug.component.sass']
})
export class DebugComponent implements OnInit {

  constructor(public wsService: WebSocketService) {}
  
  clearLog(): void{
    this.wsService.messages = []
  }
  ngOnInit(): void {}

  connectWebSocket() {
    // this.id = this.ws.getId()
  }

  nextSong() {
    this.wsService.send("next-song")
  }
  startSet(){
    this.wsService.send("start-set")
  }

}

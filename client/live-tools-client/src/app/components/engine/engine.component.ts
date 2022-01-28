import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { WebSocketService } from '../../services/web-socket/web-socket.service';

@Component({
  selector: 'app-engine',
  templateUrl: './engine.component.html',
  styleUrls: ['./engine.component.sass']
})
export class EngineComponent implements OnInit {

  constructor(public ws: WebSocketService) {}


  ngOnInit(): void {}

  connectWebSocket() {
    // this.id = this.ws.getId()
  }

  nextSong() {
    this.ws.send("next-song")
  }
  startSet(){
    this.ws.send("start-set")
  }
  nextEvent() {
    this.ws.send("next-song")
  }
}

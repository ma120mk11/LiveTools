import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { environment } from 'src/environments/environment';
import { WebSocketService } from '../../services/web-socket/web-socket.service';

@Component({
  selector: 'app-engine',
  templateUrl: './engine.component.html',
  styleUrls: ['./engine.component.sass']
})
export class EngineComponent implements OnInit {

  buttonsVisibleInRoutes: string[] = ['/engine','/engine/setlist', '/engine/lyrics', '/engine/metronome'];

  constructor(public ws: WebSocketService, private router: Router, public http: HttpClient) {this.getRoute()}


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

  insertSpeech() {
    this.http.post(`${environment.apiEndpoint}/engine/set/insert-speech`, {}).subscribe();
  }

  getRoute(): string {
    return window.location.pathname
  }
}

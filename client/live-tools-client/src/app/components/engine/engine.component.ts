import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { environment } from 'src/environments/environment';
import { WebSocketService } from '../../services/web-socket/web-socket.service';

@Component({
  selector: 'app-engine',
  templateUrl: './engine.component.html',
  styleUrls: ['./engine.component.sass']
})
export class EngineComponent implements OnInit {

  buttonsVisibleInRoutes: string[] = ['/engine','/engine/setlist', '/engine/lyrics', '/engine/metronome'];

  isLoadingNext: boolean = false;
  isLoadingSpeech: boolean = false;
  isLoadingBlackout: boolean = false;
  
  unsubscribe: Subject<boolean> = new Subject()

  constructor(public ws: WebSocketService, private router: Router, public http: HttpClient) {this.getRoute()}

  ngOnInit(): void {
    this.ws.event
      .pipe(takeUntil(this.unsubscribe))
      .subscribe({
        next: () => {
          this.isLoadingNext = false;
          this.isLoadingSpeech = false;
        }
      }
    )
  }

  connectWebSocket() {
    // this.id = this.ws.getId()
  }

  nextSong() {
    this.isLoadingNext = true;
    this.ws.send("next-song")
  }
  startSet(){
    this.ws.send("start-set")
  }
  nextEvent() {
    this.isLoadingNext = true;
    this.ws.send("next-song")
  }

  insertSpeech() {
    this.isLoadingSpeech = true;
    this.http.post(`${environment.apiEndpoint}/engine/set/insert-speech`, {}).subscribe(()=> {
      this.isLoadingSpeech = false;
    });
  }

  blackout() {
    this.isLoadingBlackout = true;
    this.http.post(`${environment.apiEndpoint}/engine/action/blackout`, {}).subscribe(()=> {
      this.isLoadingBlackout = false;
    })
  }

  ngOnDestroy(): void {
    console.log("Lyrics component destroyed")
    this.unsubscribe.next(true)
    this.unsubscribe.complete()
  }

  getRoute(): string {
    return window.location.pathname
  }
}

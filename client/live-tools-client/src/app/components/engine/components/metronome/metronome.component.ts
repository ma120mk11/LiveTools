import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSliderChange } from '@angular/material/slider';
import { Subject, takeUntil } from 'rxjs';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-metronome',
  templateUrl: './metronome.component.html',
  styleUrls: ['./metronome.component.sass']
})
export class MetronomeComponent implements OnInit {

  BLINK_TIMEOUT_MS = 80;
  AUTO_DISABLE_TIMEOUT = 10000;

  // For calculating performance
  startTime: any;
  endTime: any;

  timer: any;
  disableTimeout: any;
  beatTimeout: any;
  currentBeatDuration: number;
  isEnabled = false;
  isUpdatingTempo = false;
  hasTempo: boolean = false;

  tempo: number = 120;
  orginalTempo: number;
  currentBeat: number = 0;
  isOnBeat: boolean = false;
  isOnAccent: boolean = true;
  
  beatsUpper: number = 4;
  beatsLower: number = 4;

  unsubscribe: Subject<boolean> = new Subject()

  maxDriftMs: number = 0;


  constructor(public ws: WebSocketService, public http: HttpClient) {
    this.onActionChange();
  }

  onActionChange():void {
    this.maxDriftMs = 0;
    this.hasTempo = false // Default

    if (this.ws.activeSetlistActionId == -1) {
      // Disable
      this.isEnabled = false;
      return;
    }

    if (this.ws.activeAction.tempo == null) {
      console.log("No tempo provided for current song");
      this.orginalTempo = -1; // No tempo defined
      this.isEnabled = false;
      this.currentBeat = 0;
      return;
    }

    if (this.ws.activeAction.tempo) {
      this.tempo = this.ws.activeAction.tempo;
      this.orginalTempo = this.tempo;
      this.hasTempo = true;
      this.isEnabled = true;
      this.onTempoChange();
      this.disableTimeout = setTimeout(()=> {
        this.isEnabled = false;
        this.currentBeat = 0;
      }, this.AUTO_DISABLE_TIMEOUT)

    } else {
      this.isEnabled = false;
    }

  }

  onSlideChange(event:MatSliderChange){
    if (event.value) {
      this.setTempo(event.value)
    }
  }

  setTempo(tempo: number): void {
    this.tempo=tempo;
    this.onTempoChange();
  }

  getTempo():number {
    return this.tempo
  }

  setTempoToSong(): void {
    let songId = this.ws.activeAction.id;
    console.log("Song id: " + songId)
    if (!songId) { console.log("no song id provided"); return }
    let tempo = this.tempo;
    
    this.isUpdatingTempo = true;
    this.http.post(`${environment.apiEndpoint}/songs/${songId}/tempo`, tempo).subscribe(() => {
      this.isUpdatingTempo = false;
      this.orginalTempo = tempo;
      console.log("tempo saved!"),
      ()=>console.log("error saving tempo")
    })
  }

  ngOnInit(): void {
    this.ws.event
    .pipe(takeUntil(this.unsubscribe))
    .subscribe({
      next: () => {
        // console.log("Change!")
        // console.log(this.ws.activeAction);
        // console.log(this.ws.activeSetlistActionId);
        this.onActionChange();
      }
    })

    if (this.ws.activeAction?.tempo){
      console.log("Init, song has tempo")
      this.isEnabled = true;
      // this.onTempoChange();
      this.disableTimeout = setTimeout(()=> {
        this.isEnabled = false;
        this.currentBeat = 0;
      }, this.AUTO_DISABLE_TIMEOUT)
    }

    this.onTempoChange()
  }
  
  onTempoChange() {
    // clearInterval(this.timer);
    console.log("Tempo change: " + this.tempo);
    clearInterval(this.timer);
    this.startTime = performance.now();
    this.timer = setInterval(() => this.onBeat(), this.getBeatDuration(this.tempo, this.beatsUpper, this.beatsLower))
    this.maxDriftMs = 0
  }

  onBeat(): void {
    
    let currentTime = performance.now();
    let timeDiff = currentTime - this.startTime;
    this.startTime = performance.now();
    if (!this.isEnabled) {return}
    let drift = timeDiff - this.currentBeatDuration;
    // console.log(`${timeDiff}: ${this.currentBeatDuration}: ABS: ${timeDiff-this.currentBeatDuration}`);
    if (drift > this.maxDriftMs) {
      this.maxDriftMs = Math.round(drift);
    }

    if (!this.isEnabled) {
      this.isOnBeat = false;
      this.isOnAccent = false;
      this.currentBeat = 0;
      return
    }
    
    this.isOnBeat = true;
    
    if (this.currentBeat >= this.beatsUpper) {
      this.currentBeat = 1;
      this.isOnAccent = true;
    }
    else {
      this.isOnAccent = false;
      this.currentBeat += 1;
    }
    
   
    this.beatTimeout = setTimeout(() => {
      this.isOnBeat = false;
    }, this.BLINK_TIMEOUT_MS);
  }

  ngOnDestroy(): void {
    clearInterval(this.timer);
    clearInterval(this.beatTimeout);
    clearInterval(this.disableTimeout);
  }
  
  clearIntervals(): void {    

  }

  toggleEnable(): void {
    this.isEnabled = !this.isEnabled
    this.currentBeat = 0;

    if (this.isEnabled) {
      clearTimeout(this.disableTimeout)
      this.disableTimeout = setTimeout(()=> {
        this.isEnabled = false;
        this.currentBeat = 0;
      }, this.AUTO_DISABLE_TIMEOUT)
    }
  }

  getBeatDuration(tempo: number, top: number, bottom: number): number {
    let beatsPerSecond = tempo / 60;
    

    let currentBeatDuration = 1000 / beatsPerSecond;
    this.currentBeatDuration = currentBeatDuration;
    return currentBeatDuration
  }

}

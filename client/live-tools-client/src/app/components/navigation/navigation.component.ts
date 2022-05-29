import { Component, OnDestroy, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';


@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit, OnDestroy {

  runningSetDuration: string
  timer: any

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );
    
  constructor(
    private breakpointObserver: BreakpointObserver,
    public ws: WebSocketService,
    private http: HttpClient) {}

  releasePreview(): void{
    this.http.post(environment.apiEndpoint+"/engine/action/preview/release", {}).subscribe()
  }

  startTimer() {
    this.timer = setInterval(()=> this.runningSetDuration = this.getSetRunningDuration(), 1000);
  }
  ngOnInit(): void {
    this.startTimer()
  }

  ngOnDestroy(): void {
    clearInterval(this.timer);
  }

  getSetRunningDuration() {
    let currentTime = new Date().getTime()
    let startedOn = new Date(this.ws.setStartedOn).getTime()

    // console.log("Started on " + new Date(this.ws.setStartedOn))

    let distance = Math.abs(startedOn - currentTime);
    const hours = Math.floor(distance / 3600000);
    distance -= hours * 3600000;
    const minutes = Math.floor(distance / 60000);
    distance -= minutes * 60000;
    const seconds = Math.floor(distance / 1000);
    return `${hours}:${('0' + minutes).slice(-2)}:${('0' + seconds).slice(-2)}`;
  }
}

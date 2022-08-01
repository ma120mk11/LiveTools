import { Component, OnDestroy, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { NavigationStart, Router } from '@angular/router';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit, OnDestroy {

  runningSetDuration: string
  timer: any
  isOpened = false;
  isHandset: boolean;

  isHandset$: Observable<boolean> = this.breakpointObserver.observe([Breakpoints.TabletPortrait, Breakpoints.Handset])
    .pipe(
      map(result => {
        if (result.matches) this.isHandset = true;
        else this.isHandset = false;
        return result.matches;
      }),
      shareReplay()
    );
    
  constructor(
    private breakpointObserver: BreakpointObserver,
    private router: Router,
    public ws: WebSocketService,
    private http: HttpClient)
  {
    router.events.subscribe((next) => {
      if (this.isHandset && next instanceof NavigationStart) {
        this.isOpened = false;
      }
    });
  }

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
    const currentTime = new Date().getTime();
    const startedOn = new Date(this.ws.setStartedOn).getTime();
    let distance = Math.abs(startedOn - currentTime);
    const hours = Math.floor(distance / 3600000);
    distance -= hours * 3600000;
    const minutes = Math.floor(distance / 60000);
    distance -= minutes * 60000;
    const seconds = Math.floor(distance / 1000);
    return `${hours}:${('0' + minutes).slice(-2)}:${('0' + seconds).slice(-2)}`;
  }
}

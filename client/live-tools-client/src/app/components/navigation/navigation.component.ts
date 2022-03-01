import { Component } from '@angular/core';
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
export class NavigationComponent {

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
}

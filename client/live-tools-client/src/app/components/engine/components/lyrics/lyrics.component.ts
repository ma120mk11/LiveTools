import { HttpClient } from '@angular/common/http';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { Song } from 'src/app/components/setlist-creator/setlist-creator.component';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-lyrics',
  templateUrl: './lyrics.component.html',
  styleUrls: ['./lyrics.component.sass']
})
export class LyricsComponent implements OnInit, OnDestroy {

  lyrics: string = ""
  isLoading: boolean = true
  unsubscribe: Subject<boolean> = new Subject()

  constructor(private http: HttpClient, public ws: WebSocketService) { console.log("Lyrics constructor")}
  
  ngOnInit(): void {
    this.ws.event
      .pipe(takeUntil(this.unsubscribe))
      .subscribe({
        next: () => {
          this.lyrics = "";
          this.getLyrics();
        }
      }
    )
    this.getLyrics()
  }

  ngOnDestroy(): void {
    console.log("Lyrics component destroyed")
    this.unsubscribe.next(true)
    this.unsubscribe.complete()
  }

  getLyrics() {
    console.log("Fetching lyrics...")
    this.isLoading = true
    const url = `${environment.apiEndpoint}/engine/next-lyrics`

    this.http.get<string>(url).subscribe({
      next: data => {
        this.lyrics = data
        this.isLoading = false
      },
      error: error => {
        // TODO: Error handle error
        this.lyrics = "An error occured during fetching of the data"
      }
    })
    
  }


}

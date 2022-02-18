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

  // lyrics: string = `<p>In the day we sweat it out on the streets<br> Of a runaway American dream<br> At night we ride through the mansions of glory<br> In suicide machines<br> Sprung from cages on Highway 9<br> Chrome wheeled, fuel injected, and steppin' out over the line<br> Oh, baby this town rips the bones from your back<br> It's a death trap, it's a suicide rap<br> We gotta get out while we're young<br> 'Cause tramps like us, baby, we were born to run<br> Yes, girl, we were</p><br> <p>Wendy, let me in, I wanna be your friend<br> I wanna guard your dreams and visions<br> Just wrap your legs 'round these velvet rims<br> And strap your hands 'cross my engines<br> Together we could break this trap<br> We'll run 'til we drop, baby, we'll never go back<br> Oh, will you walk with me out on the wire?<br> 'Cause, baby, I'm just a scared and lonely rider<br> But I gotta know how it feels<br> I want to know if love is wild<br> Babe, I want to know if love is real<br> Oh, can you show me</p><br> <p>Beyond the Palace, hemi-powered drones<br> Scream down the boulevard<br> Girls comb their hair in rearview mirrors<br> And the boys try to look so hard<br> The amusement park rises bold and stark<br> Kids are huddled on the beach in the mist<br> I wanna die with you, Wendy, on the street tonight<br> In an everlasting kiss</p><br> <p>The highway's jammed with broken heroes<br> On a last chance power drive<br> Everybody's out on the run tonight<br> But there's no place left to hide<br> Together, Wendy, we can live with the sadness<br> I'll love you with all the madness in my soul<br> Oh, someday, girl, I don't know when<br> We're gonna get to that place<br> Where we really wanna go and we'll walk in the sun<br> But 'til then, tramps like us<br> Baby, we were born to run</p><br><p>Oh honey, tramps like us<br> Baby, we were born to run<br> Come on with me, tramps like us<br> Baby, we were born to run</p>`
  lyrics: string = ""
  isLoading: boolean = true
  unsubscribe: Subject<boolean> = new Subject()

  constructor(private http: HttpClient, public ws: WebSocketService) { console.log("Lyrics constructor")}
  
  ngOnInit(): void {
    this.ws.event
      .pipe(takeUntil(this.unsubscribe))
      .subscribe({
        next: () => {
          this.getLyrics()
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
    console.log(this.isLoading)
    this.isLoading = true
    const url = environment.apiEndpoint + `/engine/next-lyrics`
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

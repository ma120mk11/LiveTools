import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-lyrics',
  templateUrl: './lyrics.component.html',
  styleUrls: ['./lyrics.component.sass']
})
export class LyricsComponent implements OnInit {

  lyrics: string = `
  In the day we sweat it out on the streets
  Of a runaway American dream
  At night we ride through the mansions of glory
  In suicide machines
  Sprung from cages on Highway 9
  Chrome wheeled, fuel injected, and steppin' out over the line
  Oh, baby this town rips the bones from your back
  It's a death trap, it's a suicide rap
  We gotta get out while we're young
  'Cause tramps like us, baby, we were born to run
  Yes, girl, we were

  Wendy, let me in, I wanna be your friend
  I wanna guard your dreams and visions
  Just wrap your legs 'round these velvet rims
  And strap your hands 'cross my engines
  Together we could break this trap
  We'll run 'til we drop, baby, we'll never go back
  Oh, will you walk with me out on the wire?
  'Cause, baby, I'm just a scared and lonely rider
  But I gotta know how it feels
  I want to know if love is wild
  Babe, I want to know if love is real
  Oh, can you show me

  Beyond the Palace, hemi-powered drones
  Scream down the boulevard
  Girls comb their hair in rearview mirrors
  And the boys try to look so hard
  The amusement park rises bold and stark
  Kids are huddled on the beach in the mist
  I wanna die with you, Wendy, on the street tonight
  In an everlasting kiss

  The highway's jammed with broken heroes
  On a last chance power drive
  Everybody's out on the run tonight
  But there's no place left to hide
  Together, Wendy, we can live with the sadness
  I'll love you with all the madness in my soul
  Oh, someday, girl, I don't know when
  We're gonna get to that place
  Where we really wanna go and we'll walk in the sun
  But 'til then, tramps like us
  Baby, we were born to run
  
  Oh honey, tramps like us
  Baby, we were born to run
  Come on with me, tramps like us
  Baby, we were born to run`

  constructor() { }

  ngOnInit(): void {
  }

}

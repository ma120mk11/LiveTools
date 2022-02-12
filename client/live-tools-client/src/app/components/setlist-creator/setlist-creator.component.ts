import { Component, ChangeDetectionStrategy } from '@angular/core';
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';

export class Song {
  title: string;
  artist: string;
  lead_singer: string;
  duration: number;
  tempo?: number;
  lyrics?: string;
  key?: string;
  id?: number;
}


@Component({
  selector: 'app-setlist-creator',
  templateUrl: './setlist-creator.component.html',
  styleUrls: ['./setlist-creator.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SetlistCreatorComponent {
  songs: Song[] = [
    {
      title: "Bourbon Street",
      artist: "Hurriganes",
      lead_singer: "Philip",
      duration: 129
    },
    {
      title: "Rocking Belly",
      artist: "Hurriganes",
      lead_singer: "Philip",
      duration: 189
    },
    {
      title: "Get On",
      artist: "Hurriganes",
      lead_singer: "Philip",
      duration: 251
    },
    {
      title: "Rock And Roll",
      artist: "Led Zeppelin",
      lead_singer: "Jennifer",
      duration: 251
    },
    {
      title: "Flickorna på TV2",
      artist: "Gyllene Tider",
      lead_singer: "Jennifer",
      duration: 251
    },
    {
      title: "Born to run",
      artist: "Bruce Springsteen",
      lead_singer: "Jennifer",
      duration: 199
    }
    
    // "Bourbon Street", "Rocking Belly"
  ];

  set: Song[] = [
    // "Born to run"
  
  ];


  secToMinutes(seconds: number) {
    let minutes = Math.floor(seconds / 60);
    let rest = seconds - (minutes * 60);
    return `${minutes<10?"0":""}${minutes}:${rest<10?"0":""}${rest}`
  }

  drop(event: CdkDragDrop<Song[]>): void {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data,
          event.container.data,
          event.previousIndex,
          event.currentIndex);
    }
  }
}

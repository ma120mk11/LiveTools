import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CreateSongComponent } from './create-song/create-song.component';
import { ISong } from './song';
import { SongsService } from './songs.service';


@Component({
  selector: 'app-song-book',
  templateUrl: './song-book.component.html',
  styleUrls: ['./song-book.component.sass'],
  providers: [SongsService]
})

export class SongBookComponent implements OnInit {
  availableColumns: string[] = ["title","artist", "lead_singer", "duration", "tags", "tempo", "key"];
  displayedColumns: string[] = ["title","artist", "lead_singer", "duration", "tags", "tempo", "key"];
  songs: ISong[] = [];
  editSong: ISong | undefined // The song currently being edited
  isLoading: boolean = true

  constructor(private songService: SongsService, private dialog: MatDialog) {}
  
  ngOnInit(): void {
    this.getSongs();
  }
  
  getSongs() {
    this.songService.getSongs().subscribe(songs => {
      this.songs = songs; this.isLoading=false;
      console.log(this.songs)
    })
  }

  onRowClicked(row: any) {
    console.log("Row clicked: " + row)
  }

  onCreateSong() {
    const dialogRef = this.dialog.open(CreateSongComponent);

    dialogRef.afterClosed().subscribe(result => {
      
    })
  }

  formatDuration(seconds: number) {
    let minutes = Math.floor(seconds / 60);
    let remainder = seconds % 60;
    return `${minutes}:${remainder<10?"0":""}${remainder}`
  }


}

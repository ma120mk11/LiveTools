import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { LyricsEditorComponent } from 'src/app/lyrics-editor/lyrics-editor.component';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { environment } from 'src/environments/environment';
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
  availableColumns: string[] = ["title","artist", "lead_singer", "duration", "tags", "tempo", "key", "lyrics", "preview", "lights", "effects"];
  displayedColumns: string[] = ["title","artist", "preview", "lyrics"];

  displayExecution: string[] = ["title","artist", "preview", "lyrics", "lights", "effects"];
  displayDefault: string[] = ["title","artist", "preview", "lyrics"];

  songs: ISong[] = [];
  editSong: ISong | undefined // The song currently being edited
  isLoading: boolean = true

  constructor(private songService: SongsService, public ws: WebSocketService, private dialog: MatDialog, private http: HttpClient) {}
  
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
    console.log(this.ws.activeAction)
  }

  onCreateSong() {
    const dialogRef = this.dialog.open(CreateSongComponent);

    dialogRef.afterClosed().subscribe(result => {
      
    })
  }

  onToggleExecutionView() {
    if (this.displayedColumns == this.displayExecution) {
      this.displayedColumns = this.displayDefault
    }
    else {
      this.displayedColumns = this.displayExecution
    }
  }

  onPreview(song: ISong) {
    console.log("Preview song: " + song.title)
    this.http.post(`${environment.apiEndpoint}/songs/${song.id}/preview`, {})
    .subscribe()
  }
  
  onPreviewRelease() {
    this.http.post(`${environment.apiEndpoint}/engine/action/preview/release`, {})
    .subscribe()
  }

  onViewLyric(song: ISong) {
    const dialogRef = this.dialog.open(LyricsEditorComponent,{
      data: song
    });

    dialogRef.afterClosed().subscribe(result => {
      this.getSongs();
    })
  }

  formatDuration(seconds: number) {
    let minutes = Math.floor(seconds / 60);
    let remainder = seconds % 60;
    return `${minutes}:${remainder<10?"0":""}${remainder}`
  }


}

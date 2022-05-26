import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { LyricsEditorComponent } from 'src/app/lyrics-editor/lyrics-editor.component';
import { ISpeechAction, WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { SongExecutionEditorComponent } from 'src/app/song-execution-editor/song-execution-editor.component';
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
  EST_SPEECH_DURATION = 60
  EST_SONG_DURATION = 200

  availableColumns: string[] = ["title","artist", "lead_singer", "duration", "tags", "tempo", "key", "lyrics", "preview", "cue", "lights", "effects"];
  displayedColumns: string[] = ["title","lead_singer", "artist", "cue"];
  displayDefault:   string[] = ["title","lead_singer", "artist", "cue"];
  displayExecution: string[] = ["title", "artist", "cue", "lyrics", "lights", "effects"];

  songs: ISong[] = [];
  editSong: ISong | undefined // The song currently being edited
  isLoading: boolean = true
  showHiddenSongs: boolean = false;

  isCueMode = true;
  cueList: any[] = []

  constructor(private songService: SongsService, public ws: WebSocketService, private dialog: MatDialog, private http: HttpClient, private router: Router) {}
  
  ngOnInit(): void {
    this.getSongs();
  }
  
  getSongs() {
    this.songService.getSongs(this.showHiddenSongs).subscribe(songs => {
      this.songs = songs; this.isLoading=false;
      // console.log(this.songs)
    })
  }

  onRowClicked(row: any) {
    console.log("Row clicked: " + row)
    // console.log(this.ws.activeAction)
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

  onEditExecutionProperties(song: ISong, view: string) {
    console.log("Open " + view)
    const dialogRef = this.dialog.open(SongExecutionEditorComponent,{
      data: {
        song: song,
        view: view
      }}
    );

    dialogRef.afterClosed().subscribe(result => {
      this.getSongs();
    })
  }

  onViewLyric(song: ISong) {
    const dialogRef = this.dialog.open(LyricsEditorComponent,{
      data: song
    });

    dialogRef.afterClosed().subscribe(result => {
      this.getSongs();
    })
  }

  onToggleMode(){
    this.isCueMode = !this.isCueMode;

    if (this.isCueMode) {
      this.displayedColumns[this.displayedColumns.indexOf("preview")] = "cue";
      this.displayExecution[this.displayedColumns.indexOf("preview")] = "cue";
      this.displayDefault[this.displayedColumns.indexOf("preview")] = "cue";
      
    } else {
      this.displayedColumns[this.displayedColumns.indexOf("cue")] = "preview";
      this.displayExecution[this.displayedColumns.indexOf("cue")] = "preview";
      this.displayDefault[this.displayedColumns.indexOf("cue")] = "preview";

    }
    // if (this.isCueMode) {
    //   this.displayedColumns.splice(this.displayedColumns.indexOf("preview"));
    //   this.displayedColumns.push("cue");

    //   this.displayExecution.splice(this.displayExecution.indexOf("preview"));
    //   this.displayExecution.push("cue");

    //   this.displayDefault.splice(this.displayDefault.indexOf("preview"));
    //   this.displayDefault.push("cue");
    // } else {
    //   this.displayedColumns.splice(this.displayedColumns.indexOf("cue"));
    //   this.displayedColumns.push("preview");

    //   this.displayExecution.splice(this.displayExecution.indexOf("cue"));
    //   this.displayExecution.push("preview");

    //   this.displayDefault.splice(this.displayDefault.indexOf("cue"));
    //   this.displayDefault.push("preview");
    // }

    console.log(this.isCueMode)
  }

  onAddToCue(song: ISong) {
    this.cueList.push(song);
  }

  onRemoveFromCue(song: ISong) {
    let index = this.cueList.indexOf(song)
    if (index == -1) { return }
    console.log("Removing item " + index)
    this.cueList.splice(index, 1);
  }
  onRemoveFromCueByIndex(i: number) {
    this.cueList.splice(i,1);
  }

  onExecuteCue(): void {
    let body: number[] = []
    this.cueList.map((item) => body.push(item.id))
    this.http.post(`${environment.apiEndpoint}/engine/cue/add`, body).subscribe(() => {
      this.cueList = [];
      this.router.navigate(["/engine/setlist"])
    });
  }


  onAddSpeechToCue() {
    this.cueList.push({type: "speech", id: 1000})
  }

  getNbrOfSongsInCue(): number {
    let nbr = 0
    this.cueList.forEach((action) => {
      if (action.artist) {
        nbr += 1;
      }
    })
    return nbr
  }

  getEstimatedCueTime(): string {
    let totDuration: number = 0;
    this.cueList.forEach((action) => {
      if (action.duration) {
        totDuration += action.duration;
      } else if (action.type == "speech") {
        totDuration += this.EST_SPEECH_DURATION
      } else {
        totDuration += this.EST_SONG_DURATION;
      }
    })
    return this.formatDuration(totDuration)
  }

  existsInCuelist(song: ISong) {
    if (this.cueList.length == 0) {
      return false
    }

    let index = this.cueList.indexOf(song);
    if (index == -1) {
      return false
    } else {
      return true
    }
  }

  formatDuration(seconds: number) {
    let minutes = Math.floor(seconds / 60);
    let remainder = seconds % 60;
    return `${minutes}:${remainder<10?"0":""}${remainder}`
  }
}

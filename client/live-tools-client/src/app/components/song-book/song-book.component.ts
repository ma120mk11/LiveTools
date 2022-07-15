import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { LyricsEditorComponent } from 'src/app/lyrics-editor/lyrics-editor.component';
import { ISetlist, ISpeechAction, WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { SongExecutionEditorComponent } from 'src/app/song-execution-editor/song-execution-editor.component';
import { environment } from 'src/environments/environment';
import { CreateSongComponent } from './create-song/create-song.component';
import { ISong } from './song';
import { SongsService } from './songs.service';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { SetlistMetadataEditorComponent } from 'src/app/setlist-metadata-editor/setlist-metadata-editor.component';

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

  isSetSaved = false;

  constructor(
    private songService: SongsService, public ws: WebSocketService,
    private dialog: MatDialog, private http: HttpClient, 
    private router: Router, private route: ActivatedRoute,
    private modalRef: MatDialog)
  {
    this.route.queryParams.subscribe(query => {
      console.log(query)
      if(query['setlist_id']) {
        this.getSetlist(query['setlist_id']);
      }
    })
  }
  
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
    // console.log("Row clicked: " + row)
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
    this.http.post(`${environment.apiEndpoint}/engine/songs/${song.id}/preview`, {})
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
    console.log(this.isCueMode)
  }

  onAddToCue(song: ISong) {
    this.cueList.push(song);
    this.isSetSaved = false;
  }

  onRemoveFromCue(song: ISong) {
    let index = this.cueList.indexOf(song)
    if (index == -1) { return }
    console.log("Removing item " + index)
    this.cueList.splice(index, 1);
    this.isSetSaved = false;
  }

  onRemoveFromCueByIndex(i: number) {
    this.cueList.splice(i,1);
    this.isSetSaved = false;
  }

  onExecuteCue(): void {
    let action_ids: number[] = []
    this.cueList.map((item) => action_ids.push(item.id))

    if (!this.ws.isLoaded) {
      this.saveAsSetlist();
    }

    this.http.post(`${environment.apiEndpoint}/engine/cue/add`, action_ids).subscribe(() => {
      this.cueList = [];
      this.router.navigate(["/engine/setlist"])
    });
  }

  getSetlist(set_id: number) {
    this.http.get<ISetlist>(`${environment.apiEndpoint}/setlists/${set_id}`)
    .subscribe((setlist) => this.cueList = setlist.actions)
  }

  saveAsSetlist(prompt = false) {
    let action_ids: number[] = []
    this.cueList.map((item) => action_ids.push(item.id))

    let now = new Date()

    let setlist = {
      name: `${now.getDate()}.${now.getMonth()}.${now.getFullYear()} - ${now.getHours()}:${now.getMinutes()}`,
      actions: action_ids,
      comments: "Auto generated"
    }

    if (prompt) {
      this.modalRef.open(SetlistMetadataEditorComponent, {
        data: {
          name: setlist.name,
          comments: setlist.comments
        }
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
          setlist.name = result.name ?? setlist.name
          setlist.comments = result.comments ?? setlist.comments

          this.http.post(`${environment.apiEndpoint}/setlists`, setlist).subscribe(
            () => {this.isSetSaved = true;}, 
            () => { this.isSetSaved = false;}
          )
        }
        else {
          // On cancel
          return;
        }
      })
    } else {
      this.http.post(`${environment.apiEndpoint}/setlists`, setlist).subscribe(
        () => {this.isSetSaved = true;}, 
        () => { this.isSetSaved = false;}
      )
    }
  }

  onAddSpeechToCue(): void {
    this.cueList.push({type: "speech", id: 1000})
    this.isSetSaved = false;
  }

  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.cueList, event.previousIndex, event.currentIndex);
  }

  // Helpers ///////////////////////////////////////////////////

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

  existsInCuelist(song: ISong): boolean {
    if (this.cueList.length == 0) {
      return false
    }
    return  this.cueList.find(element => element.id === song.id);
  }

  formatDuration(seconds: number): string {
    let minutes = Math.floor(seconds / 60);
    let remainder = seconds % 60;
    return `${minutes}:${remainder<10?"0":""}${remainder}`
  }
}

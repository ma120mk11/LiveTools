import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormControl, FormGroup, NgForm } from '@angular/forms';
import { AngularEditorConfig } from '@kolkov/angular-editor';
import { environment } from 'src/environments/environment';
import { ISong } from '../components/song-book/song';
import { SongsService } from '../components/song-book/songs.service';

interface ICuelist {
  name: string,
  osc: string
}

@Component({
  selector: 'app-song-execution-editor',
  templateUrl: './song-execution-editor.component.html',
  styleUrls: ['./song-execution-editor.component.sass']
})
export class SongExecutionEditorComponent implements OnInit {

  @ViewChild('songExecForm',{static:false}) public form: NgForm;
  
  public formGroup: FormGroup
  song: ISong;
  cuelists: ICuelist[] = []
  cuelistArray: string[] = []

  constructor(@Inject(MAT_DIALOG_DATA) public data: {song: ISong, view: string}, private http: HttpClient, formBuilder: FormBuilder) {
    this.song = {...data.song}
    this.fetchCuelists()
  }
  ngOnInit(): void {}

  fetchCuelists() {
    this.http.get<{[key: string]: string}>(`${environment.apiEndpoint}/engine/lights/cuelists`)
    .subscribe((result) => {
      Object.entries(result).map((cue) => {
        this.cuelistArray.push(cue[0])
      })

      console.log(this.cuelistArray)
    })
  }

  onSubmit() {
    console.log(this.song.execution)
    this.http.post(`${environment.apiEndpoint}/songs/${this.song.id}/execution`, this.song.execution)
    .subscribe()
  }
}

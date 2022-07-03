import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormControl, FormGroup, NgForm } from '@angular/forms';
import { AngularEditorConfig } from '@kolkov/angular-editor';
import { environment } from 'src/environments/environment';
import { ISong } from '../components/song-book/song';
import { SongsService } from '../components/song-book/songs.service';
import { ILightCommand } from '../light-commands/light-commands.component';

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
  cuelists: ILightCommand[] = []
  cuelistArray: ILightCommand[] = []

  constructor(@Inject(MAT_DIALOG_DATA) public data: {song: ISong, view: string}, private http: HttpClient, formBuilder: FormBuilder) {
    this.song = {...data.song}
    this.fetchCuelists()
  }
  ngOnInit(): void {}

  fetchCuelists() {
    this.http.get<ILightCommand[]>(`${environment.apiEndpoint}/lights/commands`)
    .subscribe((result) => {
      this.cuelistArray = result;
      console.log(this.cuelistArray)
    })
  }

  onSubmit() {
    console.log(this.song.execution)
    this.http.post(`${environment.apiEndpoint}/songs/${this.song.id}/execution`, this.song.execution)
    .subscribe()
  }
}

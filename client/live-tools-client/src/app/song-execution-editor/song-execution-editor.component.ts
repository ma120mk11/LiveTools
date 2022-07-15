import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormGroup, NgForm } from '@angular/forms';
import { environment } from 'src/environments/environment';
import { ISong } from '../components/song-book/song';
import { ILightCommand } from '../light-commands/light-commands.component';


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

  constructor(@Inject(MAT_DIALOG_DATA) public data: {song: ISong, view: string}, private http: HttpClient, private dialogRef: MatDialogRef<SongExecutionEditorComponent>) {
    this.song = {...data.song}

    this.song.execution.lights.cuelist = data.song.execution.lights.cuelist.map((cue: any) => {
      if (cue.id) {
        return cue.id
      }
    })
    this.fetchCuelists()
  }

  ngOnInit(): void {}

  fetchCuelists() {
    this.http.get<ILightCommand[]>(`${environment.apiEndpoint}/lights/commands`)
    .subscribe((result) => {
      this.cuelistArray = result;
    })
  }

  onSubmit() {
    console.log(this.song.execution)
    this.http.post(`${environment.apiEndpoint}/songs/${this.song.id}/execution`, this.song.execution)
    .subscribe((result) => this.dialogRef.close())
  }
}

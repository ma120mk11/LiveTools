import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AngularEditorConfig } from '@kolkov/angular-editor';
import { environment } from 'src/environments/environment';
import { ISong } from '../components/song-book/song';
import { SongsService } from '../components/song-book/songs.service';


@Component({
  selector: 'app-lyrics-editor',
  templateUrl: './lyrics-editor.component.html',
  styleUrls: ['./lyrics-editor.component.sass']
})
export class LyricsEditorComponent implements OnInit {
  name= 'Lyrics Editor';
  htmlContent = "";
  previousContent = "";
  songId: number;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: ISong,
    private http: HttpClient
  ) {
    this.htmlContent = this.data.lyrics;
    this.previousContent = this.data.lyrics;
    this.songId = this.data.id
  }

  ngOnInit(): void { }

  onSave() {
    this.http.post(`${environment.apiEndpoint}/songs/${this.songId}/lyrics`, this.htmlContent)
    .subscribe(result => {
      console.log("Udated!")
    })
  }

  onCancel() {

  }

  editorConfig: AngularEditorConfig = {
    editable: true,
    spellcheck: true,
    height: 'auto',
    minHeight: '50vh',
    maxHeight: 'auto',
    width: 'auto',
    minWidth: '0',
    translate: 'no',
    enableToolbar: true,
    showToolbar: true,
    placeholder: 'Enter lyrics here...',
    defaultParagraphSeparator: '',
    defaultFontName: '',
    defaultFontSize: '',
    customClasses: [
      {
        name: 'Verse',
        class: 'verse',
      },
      {
        name: 'Pre-chorus',
        class: 'pre-chorus'
      },
      {
        name: 'Chorus',
        class: 'chorus'
      },
      {
        name: 'Bridge',
        class: 'bridge',
        tag: 'h1',
      },
    ],
    sanitize: true,
    toolbarPosition: 'top',
    toolbarHiddenButtons: [
      [
        'underline', 
        'strikeThrough',
        'subscript',
        'superscript',
        'insertUnorderedList',
        'insertOrderedList',
        'justifyRight',
        'justifyFull',
        'fontName'
      ],
      [
        'fontSize',
        'backgroundColor',
        'link',
        'unlink',
        'insertImage',
        'insertVideo',
        'insertHorizontalRule'
      ]
    ]
  };
}

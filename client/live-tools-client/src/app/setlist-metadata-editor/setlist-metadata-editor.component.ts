import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-setlist-metadata-editor',
  templateUrl: './setlist-metadata-editor.component.html',
  styleUrls: ['./setlist-metadata-editor.component.sass']
})
export class SetlistMetadataEditorComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }

  ngOnInit(): void {
  }

}

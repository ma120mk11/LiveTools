import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatChipInputEvent } from '@angular/material/chips';
import { map, Observable, startWith } from 'rxjs';

@Component({
  selector: 'app-create-song',
  templateUrl: './create-song.component.html',
  styleUrls: ['./create-song.component.sass']
})
export class CreateSongComponent implements OnInit {
  separatorKeysCodes: number[] = [ENTER, COMMA];
  tags: string[] = []
  tagCtrl = new FormControl();
  filteredTags: Observable<string[]>;
  allTags: string[] = ["ballad"]
  
  @ViewChild('tagInput') tagInput: ElementRef<HTMLInputElement>;

  constructor() { 
    this.filteredTags = this.tagCtrl.valueChanges.pipe(
      startWith(null),
      map((tag: string | null) => tag ? this._filter(tag):this.allTags.slice())
    );
  }

  ngOnInit(): void {
  }

  tagAdd(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add tag
    if (value) {
      this.tags.push(value);
    }
    // Clear input value
    event.chipInput!.clear();

    this.tagCtrl.setValue(null)
  }

  tagRemove(tag: string): void {
    const index = this.tags.indexOf(tag);
    if(index>=0) {
      this.tags.splice(index,1);
    }
  }

  selected(event: any): void {
    this.tags.push(event.option.viewValue);
    this.tagInput.nativeElement.value = '';
    this.tagCtrl.setValue(null);

  }
  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.allTags.filter(tag => tag.toLowerCase().includes(filterValue))
  }
}

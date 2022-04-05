import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SongExecutionEditorComponent } from './song-execution-editor.component';

describe('SongExecutionEditorComponent', () => {
  let component: SongExecutionEditorComponent;
  let fixture: ComponentFixture<SongExecutionEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SongExecutionEditorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SongExecutionEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

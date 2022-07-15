import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetlistMetadataEditorComponent } from './setlist-metadata-editor.component';

describe('SetlistMetadataEditorComponent', () => {
  let component: SetlistMetadataEditorComponent;
  let fixture: ComponentFixture<SetlistMetadataEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SetlistMetadataEditorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SetlistMetadataEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

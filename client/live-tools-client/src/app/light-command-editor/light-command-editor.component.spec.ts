import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LightCommandEditorComponent } from './light-command-editor.component';

describe('LightCommandEditorComponent', () => {
  let component: LightCommandEditorComponent;
  let fixture: ComponentFixture<LightCommandEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LightCommandEditorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LightCommandEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

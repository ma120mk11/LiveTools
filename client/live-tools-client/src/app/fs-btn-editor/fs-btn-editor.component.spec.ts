import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FsBtnEditorComponent } from './fs-btn-editor.component';

describe('FsBtnEditorComponent', () => {
  let component: FsBtnEditorComponent;
  let fixture: ComponentFixture<FsBtnEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FsBtnEditorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FsBtnEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LightCommandCreatorComponent } from './light-command-creator.component';

describe('LightCommandCreatorComponent', () => {
  let component: LightCommandCreatorComponent;
  let fixture: ComponentFixture<LightCommandCreatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LightCommandCreatorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LightCommandCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetlistsComponent } from './setlists.component';

describe('SetlistsComponent', () => {
  let component: SetlistsComponent;
  let fixture: ComponentFixture<SetlistsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SetlistsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SetlistsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

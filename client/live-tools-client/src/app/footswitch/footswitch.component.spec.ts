import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FootswitchComponent } from './footswitch.component';

describe('FootswitchComponent', () => {
  let component: FootswitchComponent;
  let fixture: ComponentFixture<FootswitchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FootswitchComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FootswitchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

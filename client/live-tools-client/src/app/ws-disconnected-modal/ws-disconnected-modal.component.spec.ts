import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WsDisconnectedModalComponent } from './ws-disconnected-modal.component';

describe('WsDisconnectedModalComponent', () => {
  let component: WsDisconnectedModalComponent;
  let fixture: ComponentFixture<WsDisconnectedModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WsDisconnectedModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WsDisconnectedModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

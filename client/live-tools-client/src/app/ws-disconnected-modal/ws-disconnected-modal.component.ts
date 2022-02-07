import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-ws-disconnected-modal',
  templateUrl: './ws-disconnected-modal.component.html',
  styleUrls: ['./ws-disconnected-modal.component.sass']
})
export class WsDisconnectedModalComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  reloadPage(): void {
    location.reload();
  }
}

import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-buttons',
  templateUrl: './buttons.component.html',
  styleUrls: ['./buttons.component.sass']
})
export class ButtonsComponent implements OnInit {

  constructor(public http: HttpClient, public ws: WebSocketService) { }

  ngOnInit(): void {
  }

  onExecutePrevious() {
    this.http.post(`${environment.apiEndpoint}/engine/set/prev`, {}).subscribe()
  }

  onResetEngine() {
    this.http.post(`${environment.apiEndpoint}/engine/reset`,{}).subscribe()
  }
}

import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { FsBtnEditorComponent } from '../fs-btn-editor/fs-btn-editor.component';

export interface IFsButtonConfig {
  action_cat: string,
  action_id: string,
  type: 'momentary' | 'switch',
  name: string,
  has_led: boolean,
  id: number,
  fs_id: string,
  btn_id: number
}

export interface IFootswitch {
  id: string,
  name: string,
  buttons: IFsButtonConfig[]
}

@Component({
  selector: 'app-footswitch',
  templateUrl: './footswitch.component.html',
  styleUrls: ['./footswitch.component.sass']
})
export class FootswitchComponent implements OnInit {
  fsArray: IFootswitch[] = [];
  selected: IFootswitch;
  fs: IFootswitch
  isEditMode: boolean = false;
  isTestMode: boolean = false;
  ws: WebSocket;

  constructor(
    public http: HttpClient, 
    private dialog: MatDialog,
    private router: Router,
    private route: ActivatedRoute)
  {
    this.route.params.subscribe( params => {
      console.log(params)
      if (params['fs_id']) {
        this.onFsChange(params['fs_id']);
      }
    });
  }

  configureSocket(): void {
    // Send footswitch config

    this.ws.onopen = () => {
      // this.ws.send(JSON.stringify(this.fs));
      this.ws.send(JSON.stringify({type: "config", data: {}}))
    }

    this.ws.onmessage = (event) => {
      console.log(event);
    }
  }

  ngOnInit(): void {
    this.http.get<IFootswitch[]>(`${environment.apiEndpoint}/footswitch`)
    .subscribe((result) => {
      this.fsArray = result;
      // this.selected = result[0];
      // this.fs=this.selected
      // this.connectFootswitch(this.fs);
    })
  }


  connectFootswitch(footswitch: IFootswitch): void {
    console.log(`Connecting to FS ${footswitch.name} (${footswitch.id})`)
    this.ws = new WebSocket(`${environment.wsEndpoint}/footswitch/${footswitch.id}`);
    this.configureSocket();
  }

  onFsChange(id: string): void {
    this.http.get<IFootswitch>(`${environment.apiEndpoint}/footswitch/${id}`)
    .subscribe((result) => {
      this.selected = result;
      this.fs = result;
      this.router.navigate(["footswitch", id])
      console.log("Changing footswitch...")
      // Only close if initialized
      if (this.ws) {
        this.ws.close();
      }
      this.fs = this.selected;
      if (this.isTestMode) {
        this.connectFootswitch(this.fs);
      }
    })
  }

  onFsChangeRequest(event: any): void {
    console.log("Changing to fs id " + event.value.id)
    this.onFsChange(event.value.id)
  }

  onBtnPress(btn: IFsButtonConfig) {
    if(this.isTestMode){
      this.ws.send(JSON.stringify({"type": "btn-change","data": {"fs_id": btn.fs_id,"btn_id": btn.btn_id, "state": 1}}));
    }
    // console.log(`Pressed ${btn.name}`);
  }

  onBtnRelease(btn: IFsButtonConfig) {
    if(this.isTestMode){
      this.ws.send(JSON.stringify({"type": "btn-change","data": {"fs_id": btn.fs_id,"btn_id": btn.btn_id, "state": 0}}));
    }
    // console.log(`Released ${btn.name}`);

  }

  onButtonEdit(button: IFsButtonConfig):void {
    const dialogRef = this.dialog.open(FsBtnEditorComponent, {data: button});
    dialogRef.afterClosed().subscribe(result => {
      if (result?.buttons) {
        this.fs = result};
      }
    );
  }

  onAddButton(): void {
    this.http.post<IFootswitch>(`${environment.apiEndpoint}/footswitch/${this.fs.id}/buttons`, {})
    .subscribe((result) => this.fs = result);
  }
}

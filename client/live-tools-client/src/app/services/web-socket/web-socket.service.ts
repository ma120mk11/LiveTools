import { Injectable } from '@angular/core';
import {webSocket, WebSocketSubject } from 'rxjs/webSocket'
import { of, Observable, Subject, Observer } from 'rxjs'
import { MatDialog } from '@angular/material/dialog';
import { WsDisconnectedModalComponent } from 'src/app/ws-disconnected-modal/ws-disconnected-modal.component';

// export const WS_ENDPOINT = "ws://localhost:8000/ws/"
// export const WS_ENDPOINT = "ws://192.168.0.24:8000/ws/"
export const WS_ENDPOINT = "ws://192.168.43.249:8000/ws/"
export const BACKED_URL = "192.168.0.249:8000"

export interface IWsMsg {
  msg_type: string;
  data: string;
  timestamp: string;
}

export interface IExecution {

  lights?: {
    cuelist?: string[]
    blackout?: boolean
    buttons?: {
      btn1?: string
      btn2?: string
      btn3?: string
      btn4?: string
    }
  }
}

export interface ISpeechAction {
  nbr: number;
  type: "speech";
  duration?: number;
  execution: IExecution;
}

export interface IAction {
  nbr: number;
  type: string;
  title?: string;
  playback?: boolean;
  song_id?: number;
  duration? : number;
  execution: IExecution;
}

export interface ISetlistMetadata {
  gig_name: string;
  set_nbr: number;
  date: string;
  name: string;
}

export interface ISetlist {
  id: number;
  name: string;
  metadata: ISetlistMetadata;
  actions: IAction[];
}

export interface IDevice {
  name: string;
  id: number;
  ip: string;
  send_port: string;
  receive_port: string;
  state: string;
}

@Injectable(
  {
  providedIn: 'root'
}
)
export class WebSocketService {
  /*
  https://developerslogblog.wordpress.com/2019/04/23/how-to-use-angular-services-to-share-data-between-components/
  */

  id = "angular-" + this.browserDetect() + "-" +this.getRandomInt(0,99);
  ws = new WebSocket(this.URL)
  
  public messages: IWsMsg[] = []
  public setlist: ISetlist
  public executionId: number = 0
  public activeAction: IAction 
  public activeSetlistActionId: number = -1
  public isLoaded = false;
  public engineStatus: string;
  public devices: IDevice[]

  public event: Subject<any> = new Subject()

  getMessages(){
    return this.messages
  }

  constructor(private dialog: MatDialog) {
    this.ws.onmessage = (event) => {
      console.log(event.data)
      let msg_obj = JSON.parse(event.data);

      switch (msg_obj.msg_type) {
        case "load-set":

          console.log("Loading set...")
          try {
            this.setlist=msg_obj.data;
            this.isLoaded = true;
            this.event.next(null);
            console.log(`Loaded set: ${this.setlist.name}`)
          } catch (error){
            console.error("Unable to load setlist");
            
          }
          break;

        case "action-config":
          this.activeAction = msg_obj.data
          break;


        case "executing-action-nbr":
          try {
            const action_id = msg_obj.data;
            if (action_id == -2) {
              // TODO: ACTION PREVEW
              this.activeSetlistActionId = action_id
            } else {
              this.activeSetlistActionId = action_id;
            }
          } catch (error) {
            console.error("Unable to set executing action id");
          }
          break;

        case "end-set":
          console.info("Set ended")
          this.isLoaded = false;
          this.activeSetlistActionId = -1;
          break;
        

        case "engine-state":
          console.debug("Engine state received")
          try {

            try {
              if (msg_obj.data.setlist?.name) {
                this.setlist = msg_obj.data?.setlist
                this.isLoaded = true
              } else {
                console.log("no set")
                this.isLoaded = false;
              }
              this.activeSetlistActionId = msg_obj.data.action_id
              this.activeAction = msg_obj.data.current_action

            } catch (error) {
              this.isLoaded = false;
              console.error("Setlist format error")
            }

            this.engineStatus = msg_obj.data.status;
            this.activeSetlistActionId = msg_obj.data.action_id;
            
          } catch (error) {
            console.error("Unable to parse engine state");
          }
          console.log(this.setlist)
          break;

        case "notification-warning":
          console.warn(msg_obj.data)

          break;

          
        case "device-state":
          try{
            this.devices = msg_obj.data
          } catch(e) {
            console.error("Error setting device states");
          }
          break;

        default:
          break;
      }


      msg_obj.data = JSON.stringify(msg_obj.data, null, 2);

      let now = new Date()
      msg_obj.timestamp = now.toLocaleTimeString()
      this.messages.unshift(msg_obj)

    }
    this.ws.onclose = () => {
      console.error("WebSocket disconnected!")
      const dialogRef = this.dialog.open(WsDisconnectedModalComponent)

    }
  }


  get URL(): string {
    return WS_ENDPOINT + this.Id
  }

  get Id(): string {
    return this.id
  }

  send(data: string) {
    this.ws.send(data);
  }

  public getNextAction(): string {
    let action = "";
    try {
      if (this.setlist.actions[this.activeSetlistActionId].title) {
        action = this.setlist.actions[this.activeSetlistActionId].title || "ERROR"
      }
      else {
        action = this.setlist.actions[this.activeSetlistActionId].type
      }
    } catch (error) {
      console.log(error)
    }
    return action
  }
  public startSet() {
    this.ws.send("start-set");
  }

  public isSetStarted() {
    return this.activeSetlistActionId > -1
  }

  private messageHandler(){}

  private browserDetect(){
                 
    let userAgent = navigator.userAgent;
    let browserName;
    
    if(userAgent.match(/chrome|chromium|crios/i)){
        browserName = "chrome";
    }else if(userAgent.match(/firefox|fxios/i)){
        browserName = "firefox";
    }  else if(userAgent.match(/safari/i)){
        browserName = "safari";
    }else if(userAgent.match(/opr\//i)){
        browserName = "opera";
    } else if(userAgent.match(/edg/i)){
        browserName = "edge";
    }else{
        browserName="No browser detection";
    }
    return browserName
  }
  private getRandomInt(min: number, max: number) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
  }
}

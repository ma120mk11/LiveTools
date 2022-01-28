import { Injectable } from '@angular/core';
import {webSocket, WebSocketSubject } from 'rxjs/webSocket'
import { of, Observable, Subject, Observer } from 'rxjs'

// export const WS_ENDPOINT = "ws://localhost:8000/ws/"
export const WS_ENDPOINT = "ws://192.168.0.24:8000/ws/"

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

  getMessages(){
    return this.messages
  }

  constructor() {
    this.ws.onmessage = (event) => {
      console.log(event.data)
      let msg_obj = JSON.parse(event.data);

      switch (msg_obj.msg_type) {
        case "load-set":

          console.log("Loading set")
          try {
            this.setlist=msg_obj.data;
            this.isLoaded = true;
            console.log(`Loaded set: ${this.setlist.name}`)
          } catch (error){
            console.error("Unable to load setlist");
            
          }
          break;

        case "action-config":
          // TODO
          break;


        case "executing-action-nbr":
          try {
            this.activeSetlistActionId = msg_obj.data;
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
              if (msg_obj.data.setlist.actions[0]['nbr'] !== 0) {
                console.error("Setlist IF check failed")
              }
              this.setlist = msg_obj.data.setlist;
              this.isLoaded = true;
            } catch (error) {
              this.isLoaded = false;
              console.error("Setlist format error")
            }

            this.engineStatus = msg_obj.data.status;
            this.activeSetlistActionId = msg_obj.data.action_id;
            
          } catch (error) {
            console.error("Unable to parse engine state");
          }
          break;

        case "notification-warning":
          console.warn("Set is not started")

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
        action = this.setlist.actions[this.activeSetlistActionId+1].title || "ERROR"
      }
    } catch (error) {

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

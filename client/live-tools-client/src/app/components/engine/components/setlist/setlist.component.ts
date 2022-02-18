import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { IAction, WebSocketService } from 'src/app/services/web-socket/web-socket.service';
import { ISetlist } from 'src/app/services/web-socket/web-socket.service';

@Component({
  selector: 'app-setlist',
  templateUrl: './setlist.component.html',
  styleUrls: ['./setlist.component.sass']
})
export class SetlistComponent implements OnInit {
  setlist: ISetlist = {
    id: 2,
    metadata: {
      gig_name: "AfterEight",
      set_nbr: 2,
      date: "20.04.2022",
      name: "Set1"
    },
    name: "Test set 1",
    actions: [
      {
        nbr: 0,
        type: "start",
        execution: {
          lights: {
            cuelist: ["start_cuelist"]
          }
        }
      },
      {
        nbr: 1,
        type: "song",
        title: "Runaway",
        song_id: 1,
        execution: {
          lights: {
            blackout: true,
            cuelist: ["high_intensity"],
            buttons: {
              btn1: "osc-command",
              btn2: "osc-command",
              btn3: "osc-command",
              btn4: "osc-command"
            }
          }
        }
      },
      {
        nbr: 2,
        type: "speech",
        duration: 5,
        execution: {
          lights: {
            cuelist: ["speaking"]
          }
        }
      },
      {
        nbr: 3,
        type: "song",
        title: "Bourbon Street",
        song_id: 5,
        execution: {
          lights: {
            cuelist: ["slow_ballad"]
          }
        }
      },

      {
        nbr: 4,
        type: "song",
        title: "Born to Run",
        execution: {
          lights: {
            cuelist: ["par_red_blue_fx", "side_par_red"]
          }
        }
      }
    ]
  }
  songs: string[]

  executingAction: number = 0;

  constructor(public ws: WebSocketService, private http: HttpClient) { }

  getSetlistName(): string {
    console.log("Evaluating..")
    let name = "ERROR"

    try {
      name = this.ws.setlist.name
    } catch (error) { }

    return name
  }

  getClass(id: number): string {
    if (id == this.ws.activeSetlistActionId) {
      return "current"
    }
    return ""
  }
  
  ngOnInit(): void {
  }

  next(): void {
    if (this.executingAction > 6) this.executingAction = 0;
    this.executingAction ++;
  }

  getSongNbr(action_nbr: number) {
    let counter = 0;
    let nbr = 0;
    this.ws.setlist.actions.forEach(action => {
      if (action.type === "song") counter ++
      if (action.nbr == action_nbr) nbr = counter
    })
    return nbr
  }

  releasePreview(): void{
    this.http.post("http://192.168.43.249:8000/"+"/engine/action/preview/release", {})
  }

}

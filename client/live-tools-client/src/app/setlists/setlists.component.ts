import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { ConfirmModalComponent } from '../confirm-modal/confirm-modal.component';
import { IAction } from '../services/web-socket/web-socket.service';


interface ISetlist {
  id: number
  name: string
  comments?: string
  actions: IAction[]
}


@Component({
  selector: 'app-setlists',
  templateUrl: './setlists.component.html',
  styleUrls: ['./setlists.component.sass']
})
export class SetlistsComponent implements OnInit {
  EST_SPEECH_DURATION = 60;
  EST_SONG_DURATION = 200;

  setlists: ISetlist[] = [];

  constructor(private http: HttpClient, private router: Router, private dialog: MatDialog,) { }

  ngOnInit(): void {
    this.getSetlists();
  }

  getSetlists() {
    this.http.get<ISetlist[]>(`${environment.apiEndpoint}/setlists`)
      .subscribe((result) => this.setlists = result)
  }

  formatDuration(seconds: number): string {
    let minutes = Math.floor(seconds / 60);
    let remainder = seconds % 60;
    return `${minutes}:${remainder < 10 ? "0" : ""}${remainder}`
  }

  getEstimatedDuration(setlist: ISetlist): string {
    let totDuration: number = 0;
    setlist.actions.forEach((action) => {
      if (action.duration) {
        totDuration += action.duration;
      } else if (action.type == "speech") {
        totDuration += this.EST_SPEECH_DURATION;
      } else {
        totDuration += this.EST_SONG_DURATION;
      }
    })
    return this.formatDuration(totDuration)
  }

  getNbrOfSongsInCue(setlist: ISetlist): number {
    let nbr = 0
    setlist.actions.forEach((action) => {
      if (action.type == "song") {
        nbr += 1;
      }
    })
    return nbr
  }

  onLoadSet(set: ISetlist) {
    this.http.post(`${environment.apiEndpoint}/engine/set/load`, set)
      .subscribe((success) => this.router.navigate(["/engine/setlist"]), (error) => console.error(error))
  }

  onEditSet(set: ISetlist) {
    this.router.navigate(["/engine/songs"], { queryParams: { setlist_id: set.id } })
  }

  onDeleteSet(set: ISetlist) {
    this.dialog.open(ConfirmModalComponent).afterClosed().subscribe(result => {
      if (result === true) {
        this.http.delete(`${environment.apiEndpoint}/setlists/${set.id}`)
          .subscribe(() => this.getSetlists());
      }
    })
  }
}

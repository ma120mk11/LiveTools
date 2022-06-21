import { HttpClient } from '@angular/common/http';
import { AfterContentInit, AfterViewInit, Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { environment } from 'src/environments/environment';
import { IFootswitch, IFsButtonConfig } from '../footswitch/footswitch.component';

export interface IFsAction {
  name: string,
  action_cat: string,
  action_id: string
}


@Component({
  selector: 'app-fs-btn-editor',
  templateUrl: './fs-btn-editor.component.html',
  styleUrls: ['./fs-btn-editor.component.sass']
})
export class FsBtnEditorComponent implements AfterContentInit {

  btnTypes = ["momentary", "switch"];

  actions: IFsAction[] = [];

  selectedAction: IFsAction;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: IFsButtonConfig,
    private dialogRef: MatDialogRef<FsBtnEditorComponent>,
    private http: HttpClient) { }
  
  matchAction(action: IFsAction, data: IFsButtonConfig) {
    console.log(action.action_id)
    console.log(data.action_id)
    return action.action_id === this.data.action_id;
  }

  ngAfterContentInit(): void {
    this.http.get<IFsAction[]>(`${environment.apiEndpoint}/footswitch/action-types`)
    .subscribe((result) => {
      this.actions = result;
      const matchedAction = this.actions.find(action => this.matchAction(action, this.data));

      if (matchedAction) {
        this.selectedAction = matchedAction
      }
      else {
        console.warn("No match found")
      }

      console.log(this.selectedAction)
    })
  }

  onActionChange(): void {
    console.log(this.selectedAction)
    this.data.action_cat = this.selectedAction.action_cat;
    this.data.name = this.selectedAction.name;
    this.data.action_id = this.selectedAction.action_id;
  }

  onSave(): void {
    this.http.post<IFootswitch>(`${environment.apiEndpoint}/footswitch/${this.data.id}/buttons/${this.data.id}`, this.data)
    .subscribe(
      (result) => {this.dialogRef.close(result)},
      (error) => {console.error("Error saving button config")})
  }
}

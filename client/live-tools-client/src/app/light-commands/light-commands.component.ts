import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { environment } from 'src/environments/environment';
import { LightCommandEditorComponent } from '../light-command-editor/light-command-editor.component';

export interface ILightCommand {
	id: number;
	name: string;
	osc_path: string;
	type?: string;
	category?: number
}

@Component({
  selector: 'app-light-commands',
  templateUrl: './light-commands.component.html',
  styleUrls: ['./light-commands.component.sass']
})
export class LightCommandsComponent implements OnInit {
	lightCommands: ILightCommand[] = [];
	displayedColumns = ['id', 'name', 'type', 'osc'];

	constructor(public http: HttpClient, private dialog: MatDialog) { }

	ngOnInit(): void {
		this.fetchItems()
	}

	fetchItems(): void {
		this.http.get<ILightCommand[]>(`${environment.apiEndpoint}/lights/commands`).subscribe((result)=> {
			this.lightCommands = result
		})
	}

	onEditLightCommand(item: ILightCommand) {
		const dialogRef = this.dialog.open(LightCommandEditorComponent, { data: item});
		dialogRef.afterClosed().subscribe(result => { })
	}
}

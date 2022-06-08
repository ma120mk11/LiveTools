import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { environment } from 'src/environments/environment';
import { ILightCommand } from '../light-commands/light-commands.component';

@Component({
	selector: 'app-light-command-editor',
	templateUrl: './light-command-editor.component.html',
	styleUrls: ['./light-command-editor.component.sass']
})
export class LightCommandEditorComponent implements OnInit {
	public formGroup: FormGroup;

	constructor(@Inject(MAT_DIALOG_DATA) public data: ILightCommand, private http: HttpClient) { 
		this.formGroup = this.createFormGroup(data);
	}

	createFormGroup(data: ILightCommand): FormGroup {
		return new FormGroup({
			name: new FormControl(data.name),
			osc_path: new FormControl(data.osc_path),
			type: new FormControl(data.type),
			category: new FormControl(data.category)
		})
	}

	getOnyxPage(str: string): string {
		const re: RegExp = /\d+/g;

		let result = str.match(re);
		if (result?.length === 2) {
			return result[0]
		}
		else return ""
	}
	getOnyxNumber(str: string): string {
		const re: RegExp = /\d+/g;

		let result = str.match(re);
		if (result?.length === 2) {
			return result[1]
		}
		else return ""
	}
	ngOnInit(): void {
	}

	onSubmit() {
		const payload = { 
			name: this.formGroup.controls['name'].value,
			osc_path: this.formGroup.controls['osc_path'].value,
			type: this.formGroup.controls['type'].value,
			category: this.formGroup.controls['category'].value
		};

		this.http.put(`${environment.apiEndpoint}/lights/commands/${this.data.id}`, payload).subscribe()
	}
}

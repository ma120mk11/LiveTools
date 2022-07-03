import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { environment } from 'src/environments/environment';
import { ILightCommand } from '../light-commands/light-commands.component';

@Component({
	selector: 'app-light-command-editor',
	templateUrl: './light-command-editor.component.html',
	styleUrls: ['./light-command-editor.component.sass']
})
export class LightCommandEditorComponent implements OnInit {

	public CUELIST_TYPES = ["COLOR", "CUELIST", "TIMECODE", "INT", "OVERRIDE"];

	public formGroup: FormGroup;

	public isLoading = false;
	public isTestingGo = false;
	public isTestingRelease = false;

	oscPath = "";

	constructor(@Inject(MAT_DIALOG_DATA) public data: ILightCommand, private http: HttpClient, private dialogRef: MatDialogRef<LightCommandEditorComponent>) { 
		this.formGroup = this.createFormGroup(data);

		this.formGroup.get("onyxPage")?.valueChanges.subscribe((value) => {
			let arr = this.formGroup.controls['osc_path'].value.match(/\d+/g);
			this.formGroup.get("osc_path")?.setValue(`/Mx/playback/page${value}/${arr[1]}/`);
		})
		this.formGroup.get("onyxNumber")?.valueChanges.subscribe((value) => {
			let arr = this.formGroup.controls['osc_path'].value.match(/\d+/g);
			this.formGroup.get("osc_path")?.setValue(`/Mx/playback/page${arr[0]}/${value -1}/`);
		})
	}

	createFormGroup(data: ILightCommand): FormGroup {
		return new FormGroup({
			name: new FormControl(data.name),
			osc_path: new FormControl(data.osc_path),
			type: new FormControl(data.type),
			category: new FormControl(data.category),
			description: new FormControl(data.description),
			onyxNumber: new FormControl(this.getOnyxNumber(data.osc_path)),
			onyxPage: new FormControl(this.getOnyxPage(data.osc_path))
		})
	}

	getOnyxPage(str: string): number {
		const re: RegExp = /\d+/g;

		let result = str.match(re);
		if (result?.length === 2) {
			return +result[0]
		}
		else return 0
	}
	getOnyxNumber(str: string): number {
		const re: RegExp = /\d+/g;

		let result = str.match(re);
		if (result?.length === 2) {
			return +result[1] + 1
		}
		else return 0
	}
	ngOnInit(): void {
	}

	testOsc(type: string) {
		if (type === "go") {
			this.isTestingGo = true;
			this.http.post(`${environment.apiEndpoint}/lights/osc/send`, {}, {params: {osc_msg: `${this.formGroup.controls['osc_path'].value}go`}})
				.subscribe(()=> this.isTestingGo = false);
		}
		else if (type==="release") {
			this.isTestingRelease = true;
			this.http.post(`${environment.apiEndpoint}/lights/osc/send`, {}, {params: {osc_msg: `${this.formGroup.controls['osc_path'].value}release`}})
				.subscribe(()=> this.isTestingRelease = false);
		}
	}

	onSave() {
		const payload = { 
			name: this.formGroup.controls['name'].value,
			osc_path: this.formGroup.controls['osc_path'].value,
			type: this.formGroup.controls['type'].value,
			category: this.formGroup.controls['category'].value
		};
		this.isLoading = true;
		this.http.put<ILightCommand>(`${environment.apiEndpoint}/lights/commands/${this.data.id}`, payload)
		.subscribe((result) => { 
			this.data = result; this.isLoading = false; 
			this.dialogRef.close();
		})
	}
}

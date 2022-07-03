import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ILightCommand } from '../light-commands/light-commands.component';

@Component({
  selector: 'app-light-command-creator',
  templateUrl: './light-command-creator.component.html',
  styleUrls: ['./light-command-creator.component.sass']
})
export class LightCommandCreatorComponent implements OnInit {

	public CUELIST_TYPES = ["COLOR", "CUELIST", "TIMECODE", "OVERRIDE"];

	public formGroup: FormGroup;

	public isLoading = false;
	public isTestingGo = false;
	public isTestingRelease = false;

	data: ILightCommand;

	oscPath = "";

	constructor(private http: HttpClient) {
		this.data.id = 0;
		this.data.category = 0;
		this.data.description = "";
		this.data.name = "";
		this.data.osc_path ="/Mx/playback/page1/0";
		this.data.type = "";

		this.formGroup = this.createFormGroup();

		this.formGroup.get("onyxPage")?.valueChanges.subscribe((value) => {
			let arr = this.formGroup.controls['osc_path'].value.match(/\d+/g);
			this.formGroup.get("osc_path")?.setValue(`/Mx/playback/page${value}/${arr[1]}/`);
		})
		this.formGroup.get("onyxNumber")?.valueChanges.subscribe((value) => {
			let arr = this.formGroup.controls['osc_path'].value.match(/\d+/g);
			this.formGroup.get("osc_path")?.setValue(`/Mx/playback/page${arr[0]}/${value -1}/`);
		})
	}

	createFormGroup(): FormGroup {
		return new FormGroup({
			name: new FormControl(),
			osc_path: new FormControl("/Mx/playback/page1/0"),
			type: new FormControl(),
			category: new FormControl(),
			description: new FormControl(),
			onyxNumber: new FormControl(this.getOnyxNumber("/Mx/playback/page1/0")),
			onyxPage: new FormControl(this.getOnyxPage("/Mx/playback/page1/0"))
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

	executeOsc(type: string) {
		if (type === "go") {
			// this.http.post(`${environment.apiEndpoint}/`)
		}
	}
	onSubmit() {
	// 	const payload = { 
	// 		name: this.formGroup.controls['name'].value,
	// 		osc_path: this.formGroup.controls['osc_path'].value,
	// 		type: this.formGroup.controls['type'].value,
	// 		category: this.formGroup.controls['category'].value
	// 	};
	// 	this.isLoading = true;
	// 	this.http.put<ILightCommand>(`${environment.apiEndpoint}/lights/commands/${this.data.id}`, payload)
	// 	.subscribe(
	// 		(result) => { this.data = result; this.isLoading = false;})
	}
}

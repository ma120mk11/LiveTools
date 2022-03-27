import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { IDevice } from 'src/app/services/web-socket/web-socket.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-configure-device',
  templateUrl: './configure-device.component.html',
  styleUrls: ['./configure-device.component.sass']
})
export class ConfigureDeviceComponent implements OnInit {

  public deviceEditForm: FormGroup

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: IDevice,
    private http: HttpClient
  ) { 
    this.deviceEditForm = this.createFormGroup(data)
  }

  createFormGroup(data: IDevice){
    return new FormGroup({
      ip: new FormControl(data.ip),
      receive_port: new FormControl(data.receive_port)
    })
  }

  onSubmit(){
    console.log("Submitted: ")
    console.log(this.deviceEditForm.controls['ip'].value)
    console.log(this.deviceEditForm.controls['receive_port'].value)

    const url = `${environment.apiEndpoint}/devices/${this.data.id}`
    
    this.http.patch(url, {
      ip: this.deviceEditForm.controls['ip'].value,
      receive_port: this.deviceEditForm.controls['receive_port'].value
    }).subscribe()
  }

  ngOnInit(): void {
  }

}

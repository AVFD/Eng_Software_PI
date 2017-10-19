import { DbService } from './../db-service.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-administrador-form-edit',
  templateUrl: './administrador-form-edit.component.html',
  styleUrls: ['./administrador-form-edit.component.css']
})
export class AdministradorFormEditComponent implements OnInit {
  adminSelected = { };
  id:string;
  constructor(
    private routeActive:ActivatedRoute,
    private dbService:DbService
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService
    .getAdministrador(this.id) 
    .map(res=> res.json())
    .subscribe((data)=>{
      this.adminSelected = data;
    });
  }
  onSubmit(form){
    this.adminSelected = {
      'id': this.id,
      'name': form.value.name,
      'login_name': form.value.login_name,
      'password': form.value.password,
      'email': form.value.email
    }
    this.dbService.updateAdministrador(this.adminSelected).subscribe();
  }



}

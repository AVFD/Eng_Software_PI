import { DbService } from './../db-service.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-administrador-form',
  templateUrl: './administrador-form.component.html',
  styleUrls: ['./administrador-form.component.css']
})
export class AdministradorFormComponent implements OnInit {
  private adminJson:any = {  };
  constructor(private dbService:DbService) { }

  ngOnInit() {
  }

  onSubmit(form){
    this.adminJson = {
      'name': form.value.name,
      'login_name': form.value.login_name,
      'password': form.value.password,
      'email': form.value.email
    }
    console.log(this.dbService.adicionarAdm(this.adminJson).subscribe());

  }
}

import { DbService } from './../../db.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-adm-edit',
  templateUrl: './adm-edit.component.html',
  styleUrls: ['./adm-edit.component.css']
})
export class AdmEditComponent implements OnInit {
  adminSelected = { };
  id:string;
  constructor(
    private routeActive:ActivatedRoute,
    private dbService:DbService,
    private router:Router
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService
    .getAdministrador(this.id) 
    .map(res=> res.json())
    .subscribe((data)=>{
      this.adminSelected = data.admins[0];
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
    console.log(this.adminSelected)
    this.dbService.updateAdministrador(this.adminSelected).toPromise()
    .then(res=>{
      alert('Administrador editado com sucesso!')
      this.router.navigate(['/adm'])
    })
    .catch(er => alert('Erro ao editar.'));
  }
  cancel(){
    this.router.navigate(['/adm'])
  }
}

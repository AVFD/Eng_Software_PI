import { DbService } from './../../db.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-adm-form',
  templateUrl: './adm-form.component.html',
  styleUrls: ['./adm-form.component.css']
})
export class AdmFormComponent implements OnInit {
  private admin:any ={
    'name':'',
    'email':'',
    'login_name':'',
    'password':''
  }
  constructor(
    private router:Router,
    private dbService:DbService
  ) { }

  ngOnInit() {
  }
  onSubmit(form){
    if(form.valid){
      console.log(this.admin)
      this.dbService.adicionarAdm(this.admin)
      .toPromise()
      .then(response => {
        alert('Cadastro concluido com sucesso.');
        this.router.navigate(['/adm']);
      })
      .catch(er =>{
        if(er.status === 409){
          alert('Usuário ou email ja cadastrados!')
        }else if(er.status === 0){
          alert('Não foi possivel conectar com o banco, tente novamente mais tarde!');
        }
      });

    }
  }
  
  cancel(){
    this.router.navigate(['/adm']);
  }
}

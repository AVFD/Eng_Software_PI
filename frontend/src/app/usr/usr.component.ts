import { Router } from '@angular/router';
import { DbService } from './../db.service';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-usr',
  templateUrl: './usr.component.html',
  styleUrls: ['./usr.component.css']
})
export class UsrComponent implements OnInit {
  usrJsonBackEnd:any = [];
  profissoes = ['Zelador(a)', 'Professor(a)', 'Estudante', 'Funcionário(a)'];
  profissao:string;
  constructor(
    private router:Router,
    private dbService:DbService
  ) { }
  onSubmit(form){
    switch(this.profissao){
      case 'Zelador(a)':{
        this.dbService.getFilterUser('zelador')
        .map(res=> res.json())
        .toPromise()
        .then(data => this.usrJsonBackEnd = data.users)
        .catch(() => alert('Não há nenhum Zelador cadastrado!'))
        break;
      }
      case 'Professor(a)': {
        this.dbService.getFilterUser('professor')
        .map(res=> res.json())
        .toPromise()
        .then(data => this.usrJsonBackEnd = data.users)
        .catch(() => alert('Não há nenhum Professor cadastrado!'))
        break;
      }
      case 'Estudante':{
        this.dbService.getFilterUser('estudante')
        .map(res=> res.json())
        .toPromise()
        .then(data => this.usrJsonBackEnd = data.users)
        .catch(() => alert('Não há nenhum Estudante cadastrado!'))
        break;
      }
      case 'Funcionário(a)':{
        this.dbService.getFilterUser('funcionario')
        .map(res=> res.json())
        .toPromise()
        .then(data => {
          this.usrJsonBackEnd = data.users
        })
        .catch(() => alert('Não há nenhum Funcionário cadastrado!'))
        break;
      }
      case 'Todos':{
        this.dbService
        .getUsers()
        .map(res => res.json())
        .toPromise()
        .then(data => {
          this.usrJsonBackEnd = data.users
        })
        break;
      }
    }
  }
  ngOnInit() {
    this.dbService
    .getUsers()
    .map(res => res.json())
    .toPromise()
    .then(data => {
      this.usrJsonBackEnd = data.users;
      this.profissao = 'Todos';

    })
  }
  removeUser(id){
    if(confirm('Tem certeza que você deseja excluir?')){
      this.dbService.removerUser(this.usrJsonBackEnd[id].id).subscribe();
      this.usrJsonBackEnd.splice(id, 1);
    }
  }
  editar(id){
    this.router.navigate(['usr', id]);
  }
  filterSelected(profissao){
    this.profissao = profissao;
    this.onSubmit(null);
  }
}

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

  constructor(
    private router:Router,
    private dbService:DbService
  ) { }

  ngOnInit() {
    this.dbService
    .getUsers()
    .map(res => res.json())
    .toPromise()
    .then(data => {
      this.usrJsonBackEnd = data.users
    })
    .catch(er => alert('Erro: '+er.status+' ao listar Usuários!'));
  }
  removeUser(id){
    this.dbService.removerUser(this.usrJsonBackEnd[id].id).subscribe();
    this.usrJsonBackEnd.splice(id, 1);
  }
  editar(id){
    this.router.navigate(['usr', id]);
  }
  
}

import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { DbService } from './../db.service';

@Component({
  selector: 'app-adm',
  templateUrl: './adm.component.html',
  styleUrls: ['./adm.component.css']
})
export class AdmComponent implements OnInit {
  adminsJsonBackEnd:any = []
  constructor(
    private dbService: DbService,
    private router:Router
  ) { }

  ngOnInit() {
    this.dbService
    .getAdministradores() 
    .map(res=> res.json())
    .toPromise()
    .then((data)=>{
      this.adminsJsonBackEnd = data.admins
    })      
  }
  
  deletarAdm(id){
    this.dbService.removerAdm(this.adminsJsonBackEnd[id].id).subscribe();
    this.adminsJsonBackEnd.splice(id, 1);
  }
  editar(id){
    this.router.navigate(['adm', id]);
  }
}

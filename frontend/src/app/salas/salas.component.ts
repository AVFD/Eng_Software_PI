import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { DbService } from './../db.service';

@Component({
  selector: 'app-salas',
  templateUrl: './salas.component.html',
  styleUrls: ['./salas.component.css']
})
export class SalasComponent implements OnInit {
  salasJsonBackEnd:any = [];
  constructor(
    private dbService:DbService,
    private router:Router
  ) { }

  ngOnInit() {
    this.dbService
    .getSalas() 
    .map(res=> res.json())
    .toPromise()
    .then((data)=>{
      this.salasJsonBackEnd = data.laboratories
    })
  }
  removeSala(id){
    if(confirm('Tem certeza que você deseja excluir?')){
      console.log(this.salasJsonBackEnd)
      this.dbService.removerSala(this.salasJsonBackEnd[id].id).subscribe();
      this.salasJsonBackEnd.splice(id, 1);
    }
  }
  editarSala(id){
    this.router.navigate(['salas', id]);
  }
}

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
    .subscribe((data)=>{
      this.salasJsonBackEnd = data
    });
  }
  removeSala(id){
    this.dbService.removerSala(id).subscribe();
    this.ngOnInit();
    this.ngOnInit();
  }
  editarSala(id){
    this.router.navigate(['salas', id]);
  }
}

import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { DbService } from './../../db.service';
@Component({
  selector: 'app-salas-edit',
  templateUrl: './salas-edit.component.html',
  styleUrls: ['./salas-edit.component.css']
})
export class SalasEditComponent implements OnInit {
  sala:any = {}
  id:number;
  constructor(
    private routeActive:ActivatedRoute,
    private dbService:DbService
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService.getSala(this.id)
    .map(res=>res.json())
    .toPromise()
    .then(data => {
      this.sala = data.laboratory
    })
    .catch(er => alert('Erro: '+er.status+' ao listar as salas'))
  }

}

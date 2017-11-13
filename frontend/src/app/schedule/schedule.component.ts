import { DbService } from './../db.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.css']
})
export class ScheduleComponent implements OnInit {
  salaSelecionada:string;
  diaSelecionado:string;
  salas:any = [];
  dSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'];
  constructor(
    private route:Router,
    private dbService:DbService
  ) { }

  ngOnInit() {
    this.dbService.getSalas()
    .map(res => res.json())
    .toPromise()
    .then(data => {
      this.salas = data.laboratories
    })
  }
  onSubmit(form){
    
  }
  salaSelected(sala){
    this.salaSelecionada = sala;
    console.log(this.salaSelecionada)  
  }
  diaSelected(dia){
    this.diaSelecionado = dia;
    console.log(this.diaSelecionado)
  }
}

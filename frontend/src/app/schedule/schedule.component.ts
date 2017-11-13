import { DbService } from './../db.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.css']
})
export class ScheduleComponent implements OnInit {
  //itens comboBox selecionados
  salaSelecionada:string;
  diaSelecionado:string;

  //itens do comboBox
  salas:any = [];
  dSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'];

  schedules:any = [];
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
    this.dbService.getScheduleByDay(this.diaSelecionado, this.salaSelecionada)
    .map(res => res.json())
    .toPromise()
    .then(data => this.schedules = data.schedules)
    .catch(er =>{
      if(er.status === 404){
        alert('A sala não possui nenhum horário agendado nesse dia!');
      }
      else if(er.status === 0){
        alert('Selecione uma sala e um dia!');  
      }
    });
  }
  salaSelected(sala){
    this.salaSelecionada = sala;
  }
  diaSelected(dia){
    this.diaSelecionado = dia;
  }
  deletarSche(id){
    if(confirm('Tem certeza que você deseja excluir?')){
      this.dbService.removerSche(this.schedules[id].id).subscribe();
      this.schedules.splice(id, 1);
    }
  }
  editar(id){
    this.route.navigate(['/schedule', id]);
  }
}

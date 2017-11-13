import { DbService } from './../../db.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { IMultiSelectTexts, IMultiSelectOption, IMultiSelectSettings } from 'angular-2-dropdown-multiselect';

@Component({
  selector: 'app-schedule-form',
  templateUrl: './schedule-form.component.html',
  styleUrls: ['./schedule-form.component.css']
})
export class ScheduleFormComponent implements OnInit {
  profissaoSelecionada:string;
  profissoes = ['Zelador(a)', 'Professor(a)', 'Estudante', 'Funcionário(a)'];
  dSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'];
  schedule:any;
  diaSelecinado:string;
  salas:string;
  constructor(
    private route:Router,
    private dbService:DbService
  ) { }

  onSubmit(form){
    if(form.valid){
      this.schedule = {
        'start': form.value.inicio,
        'end': form.value.termino,
        'purpouse': form.value.porpose,
        'day_of_the_week': this.diaSelecinado,
        'profession': this.profissaoSelecionada,
        'laboratory_id': 2
      }
    }
  }
  ngOnInit() {
    this.dbService.getSalas()
    .map(res=> res.json())
    .toPromise()
    .then(data => {
      this.salas = data.laboratories
    })
    .catch(er => alert('Erro: '+er.status+' ao listar salas!'))
  }
  cancel(){
    this.route.navigate(['/schedule']);
  }
  profissaoSelected(profissao){
    this.profissaoSelecionada = profissao;
  }
  diaSelected(dia){
    this.diaSelecinado = dia;
  }
  salaSelected(sala){
    console.log(sala)
  }
}

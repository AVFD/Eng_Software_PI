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
  //selecionar ComboBox
  profissaoSelecionada:string;
  diaSelecinado:string;
  salaSelectionada:number;
  //valor ComboBox
  profissoes = ['Zelador(a)', 'Professor(a)', 'Estudante', 'Funcionário(a)'];
  dSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'];
  salas:string;
  //valor para passar no json
  schedule:any;
  constructor(
    private route:Router,
    private dbService:DbService
  ) { }

  onSubmit(form){
    if(form.valid){
      this.schedule = {
        'start': form.value.inicio,
        'end': form.value.termino,
        'purpouse': form.value.purpouse,
        'day_of_the_week': this.diaSelecinado,
        'profession': this.profissaoSelecionada,
        'laboratory_id': this.salaSelectionada
      }
      console.log(this.schedule)
      this.dbService.adicionarSchedule(this.schedule)
      .toPromise()
      .then(()=>{
        alert('Schedule cadastrada com sucesso!');
        this.route.navigate(['/schedule'])
      })
      .catch(er => alert('Erro: '+er.status+' ao adicionar Schedule'));
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
    this.salaSelectionada = sala;
  }
}

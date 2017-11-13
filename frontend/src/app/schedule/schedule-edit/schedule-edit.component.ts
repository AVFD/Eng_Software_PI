import { DbService } from './../../db.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-schedule-edit',
  templateUrl: './schedule-edit.component.html',
  styleUrls: ['./schedule-edit.component.css']
})
export class ScheduleEditComponent implements OnInit {
  diaSelecionado:string;
  profissaoSelecionada:string;
  id:number;
  lab_id:number;
  schedule:any = {
    'day_of_the_week': '',
    'end': '',
    'laboratory_id': '',
    'profession': '',
    'purpouse': '',
    'start': ''
  };
  //valor ComboBox
  profissoes = ['Zelador(a)', 'Professor(a)', 'Estudante', 'Funcionário(a)'];
  dSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'];
  constructor(
    private route:Router,
    private dbService:DbService,
    private routeActive:ActivatedRoute
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService.getSchedule(this.id)
    .map(res => res.json())
    .toPromise()
    .then(data => {
      this.schedule = data.schedules[0];
      this.lab_id = this.schedule.laboratory_id
      this.diaSelecionado = this.schedule.day_of_the_week;
      this.profissaoSelecionada = this.schedule.profession;
    })
    .catch(er => alert('Erro: '+er.status+' ao pegar schedule'));
    
  }
  onSubmit(form){
    this.schedule = {
      'id': this.id,
      'profession': this.profissaoSelecionada,
      'day_of_the_week': this.diaSelecionado,
      'end': form.value.termino,
      'laboratory_id': this.lab_id,
      'purpouse': form.value.purpouse,
      'start': form.value.inicio
    };
    this.dbService.updateSchedule(this.schedule)
    .map(res => res.json())
    .toPromise()
    .then((res) => {
      alert('Reserva de horários editada com sucesso!')
      this.route.navigate(['/schedule']);
    })
    .catch(er => {
      alert('Erro: '+er.status+' ao editar!');
    })
  } 
  profissaoSelected(profissao){
    this.profissaoSelecionada = profissao;
  }
  diaSelected(dia){
    this.diaSelecionado = dia;
  }
  cancel(){
    this.route.navigate(['/schedule']);
  }
}

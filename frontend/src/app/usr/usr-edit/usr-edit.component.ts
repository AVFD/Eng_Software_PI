import { DbService } from './../../db.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts} from 'angular-2-dropdown-multiselect';
@Component({
  selector: 'app-usr-edit',
  templateUrl: './usr-edit.component.html',
  styleUrls: ['./usr-edit.component.css']
})
export class UsrEditComponent implements OnInit {
  optionsModel = [];
  profissoes = ['Zelador(a)', 'Professor(a)', 'Estudante', 'Funcionário(a)'];
  user:any = {
    'id':'',
    'email':'',
    'name': '',
    'internal_id': '',
    'profession': '',
    'allowed_lab_id': []
    };
  profissao:string;
  id:number;
  constructor(
    private dbService:DbService,
    private router:Router,
    private routeActive:ActivatedRoute
  ) { }

  // Settings configuration
  mySettings: IMultiSelectSettings = {
    showCheckAll: true,
    showUncheckAll: true,
    isLazyLoad: true,
    checkedStyle: 'fontawesome',
    buttonClasses: 'btn btn-primary',
    dynamicTitleMaxItems: 6,
    displayAllSelectedText: true
  };

// Text configuration
  myTexts: IMultiSelectTexts = {
    checkAll: 'Marcar todos',
    uncheckAll: 'Desmarcar todos',
    checked: 'Item marcado!',
    searchEmptyResult:'Vazio...',
    checkedPlural: 'Itens marcados!',
    defaultTitle: 'Selecione as Salas',
    allSelected: 'Todos selecionados!',
  };

// Labels / Parents
  myOptions: IMultiSelectOption[];
  onSubmit(form){
    if(form.valid){
      this.user.profession = this.profissao
      this.user.allowed_lab_id = this.optionsModel
      this.user.id = this.id
      this.dbService.updateUser(this.user)
      .toPromise()
      .then(res => {
        alert('Usuário editado com sucesso!')
        this.router.navigate(['/usr'])
      })
      .catch(er =>{
        if(er.status === 400){
          alert('Usuário não encontrado!');
          this.router.navigate(['/usr']);
        }else
          alert('Erro: '+er.status+' ao editar usuário!');
      });
    }
  }
  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService.getUser(this.id)
    .map(res=>res.json())
    .toPromise()
    .then(data => {
      this.user.name = data.users[0].name
      this.user.email = data.users[0].email
      this.user.internal_id = data.users[0].internal_id
      this.user.profession = data.users[0].profession
      data.users[0].allowed_lab.forEach(element => {
        this.user.allowed_lab_id.push(element.laboratory_id)
      });
      this.optionsModel = this.user.allowed_lab_id
      this.profissao = this.user.profession
    })
    .catch(er => alert('Erro: '+er.status+' ao listar as salas'))

    this.dbService.getSalas()
    .map(res=>res.json())
    .toPromise()
    .then(data => {
      this.myOptions = data.laboratories
    })
    .catch(er => alert('Erro: '+er.status+' ao listar as salas'))
  }

  cancel(){
    this.router.navigate(['usr']);
  }
  profissaoSelected(profissao){
    this.profissao = profissao
  }

}

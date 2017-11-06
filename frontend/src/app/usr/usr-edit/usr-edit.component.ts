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
  profissoes = ['funcionario', 'estudante', 'zelador', 'professor'];
  user = {}
  profissao:string;
  salas = []
  id:string;
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
    buttonClasses: 'btn btn-default btn-block',
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
      for(let j = 0; j < this.optionsModel.length; j++){
        this.salas.push(this.myOptions[j].name);
      }
      this.user = {
        'email': form.value.email,
        'internal_id': form.value.ri,
        "security_key": form.value.rfid,
        "name": form.value.name,
        "profession": this.profissao,
        "permission": this.salas
      };
      this.dbService.adicionarUser(this.user).toPromise()
      .then(res => {
        alert('Usuário editado com sucesso!')
        this.router.navigate(['/usr'])
      })
      .catch(er =>{
        alert('Erro ao editar usuário!');
        // if(er.status === 409){
        //   alert('Usuário ou email ja cadastrados!')
        // }else if(er.status === 0){
        //   alert('Não foi possivel conectar com o banco, tente novamente mais tarde!');
        // }
      });
    }
  }
  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService.getUser(this.id).map(res=>res.json()).toPromise()
    .then(data => {
      this.user = data.user
    })
    .catch(er => alert('Erro: '+er.status+' ao listar as salas'))

    this.dbService.getSalas().map(res=>res.json()).toPromise()
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

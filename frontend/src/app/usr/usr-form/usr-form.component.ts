import { DbService } from './../../db.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts} from 'angular-2-dropdown-multiselect';
@Component({
  selector: 'app-usr-form',
  templateUrl: './usr-form.component.html',
  styleUrls: ['./usr-form.component.css']
})
export class UsrFormComponent implements OnInit {
  optionsModel = [];
  profissao:string;
  profissoes = ['Zelador(a)', 'Professor(a)', 'Estudante', 'Funcionário(a)'];
  user:any = {};
  constructor(
    private dbService:DbService,
    private router:Router
  ) { }

  // Settings configuration
  mySettingx: IMultiSelectSettings = {
    showCheckAll: true,
    showUncheckAll: true,
    isLazyLoad: true,
    checkedStyle: 'fontawesome',
    buttonClasses: 'btn btn-primary btn-block',
    dynamicTitleMaxItems: 10,
    displayAllSelectedText: true
  };

// Text configuration
  myTexts: IMultiSelectTexts = {
    checkAll: 'Marcar todos',
    uncheckAll: 'Desmarcar todos',
    checked: 'Item marcado!',
    checkedPlural: 'Itens marcados!',
    defaultTitle: 'Selecione as salas',
    allSelected: 'Todos selecionados!',
  };

// Labels / Parents
  myOptions: IMultiSelectOption[];
  
  onSubmit(form){
    if(form.valid){
      this.user = {
        'name':form.value.name,
        'email':form.value.email,
        'internal_id':form.value.ri,
        'security_key':form.value.rfid,
        'allowed_lab_id':this.optionsModel,
        'profession':this.profissao
      }
      this.dbService.adicionarUser(this.user).toPromise()
      .then(res => {
        alert('Usuário cadastrado com sucesso!')
        this.router.navigate(['/usr'])
      })
      .catch(er =>{
        alert('Erro '+er.status+' ao adicionar usuário!');
        // if(er.status === 409){
        //   alert('Usuário ou email ja cadastrados!')
        // }else if(er.status === 0){
        //   alert('Não foi possivel conectar com o banco, tente novamente mais tarde!');
        // }
      });
    }
  }
  ngOnInit() {
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
    this.profissao = profissao;
  }
}

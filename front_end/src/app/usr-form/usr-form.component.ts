import { DbService } from './../db-service.service';
import { Component, OnInit } from '@angular/core';
import { IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts} from 'angular-2-dropdown-multiselect';


@Component({
  selector: 'app-usr-form',
  templateUrl: './usr-form.component.html',
  styleUrls: ['./usr-form.component.css']
})
export class UsrFormComponent implements OnInit {
  private salas_Selected = [];
  constructor(
    private dbService:DbService,
  ) { }
  
// Settings configuration
  mySettings: IMultiSelectSettings = {
    showCheckAll: true,
    showUncheckAll: true,
    isLazyLoad: true,
    checkedStyle: 'fontawesome',
    buttonClasses: 'btn btn-default btn-block',
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


  ngOnInit() {
    this.dbService.getSalas()
    .map(res=> res.json())
    .subscribe(data=>{
      this.myOptions = data.laboratories;
    });
  }
  onSubmit(form){
    if (form.valid) {
      
      
    }
  }

}

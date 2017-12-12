import { Component, OnInit } from '@angular/core';
import { validateConfig } from '@angular/router/src/config';

@Component({
  selector: 'app-relatorio',
  templateUrl: './relatorio.component.html',
  styleUrls: ['./relatorio.component.css']
})
export class RelatorioComponent implements OnInit {
  data_valida = false;
  data_inicio = '';
  data_fim = '';
  private mask = [/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/];
  constructor() { }

  ngOnInit() {
  }

  validarData(data){
    var datav = data.split("/");
    if(datav[0] > 0 && datav[0] <= 31){
      if(datav[1] > 0 && datav[1] <= 12){
        if(datav[2] >= 2017){
          return true;
        }
      }
    }
    return false;
  }

  onSubmit(form){
    if(form.valid){
      if(this.validarData(this.data_inicio) && this.validarData(this.data_fim)){
        this.data_valida = true;
      }
      else
        alert('Digite uma data válida!');
      
    }
  }
}

import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { DbService } from './../../db.service';

@Component({
  selector: 'app-salas-form',
  templateUrl: './salas-form.component.html',
  styleUrls: ['./salas-form.component.css']
})
export class SalasFormComponent implements OnInit {
  sala:any ={}
  constructor(
    private dbService: DbService,
    private router:Router
  ) { }

  ngOnInit() {
  }
  onSubmit(form){
    this.sala = {
      'name': form.value.name
    };
    this.dbService.adicionarSala(this.sala)
    .toPromise()
    .then(response => {
      alert('Sala cadastrada com sucesso!');
      this.router.navigate(['/salas']);
    })
    .catch(er => {
      if(er.status === 409){
        alert('Essa sala já existe!');
      }
    })
  }
  cancel(){
    this.router.navigate(['/salas']);
  }

}

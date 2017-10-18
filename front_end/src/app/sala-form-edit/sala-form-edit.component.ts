import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { SalasService } from './../salas/salas.service';
@Component({
  selector: 'app-sala-form-edit',
  templateUrl: './sala-form-edit.component.html',
  styleUrls: ['./sala-form-edit.component.css']
})
export class SalaFormEditComponent implements OnInit {
  salaSelected = { };
  id:string;
  constructor(
    private routeActive:ActivatedRoute,
    private salasService:SalasService
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.salasService
    .getSala(this.id) 
    .map(res=> res.json())
    .subscribe((data)=>{
      this.salaSelected = data
    });
  }
  onSubmit(form){
    this.salaSelected = {
      'id': this.id,
      'name': form.value.name
    }
    this.salasService.updateSala(this.salaSelected).subscribe();
  }

}

import { ActivatedRoute, Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { DbService } from './../../db.service';
@Component({
  selector: 'app-salas-edit',
  templateUrl: './salas-edit.component.html',
  styleUrls: ['./salas-edit.component.css']
})
export class SalasEditComponent implements OnInit {
  sala:any = {
    'name':''
  }
  id:number;
  constructor(
    private routeActive:ActivatedRoute,
    private dbService:DbService,
    private route:Router
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService.getSala(this.id)
    .map(res=>res.json())
    .toPromise()
    .then(data => {
      this.sala = data.laboratories[0]
    })
  }
  onSubmit(form){
    if(form.valid){
      this.dbService.updateSala(this.sala)
      .toPromise()
      .then(res=> {
        alert('Sala editada com sucesso!')
        this.route.navigate(['/salas'])
      })
      .catch(er => {
        if(er.status === 409)
          alert('Sala já cadastrada!');
      });
    }
  }
  cancel(){
    this.route.navigate(['/salas'])
  }
}

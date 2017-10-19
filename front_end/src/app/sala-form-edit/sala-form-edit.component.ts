import { DbService } from './../db-service.service';
import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

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
    private dbService:DbService
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params:any)=>this.id = params['id']);
    this.dbService
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
    this.dbService.updateSala(this.salaSelected).subscribe();
  }

}

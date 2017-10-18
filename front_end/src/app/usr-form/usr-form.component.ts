import { SalasService } from './../salas/salas.service';
import { UsrService } from './../usr/usr.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-usr-form',
  templateUrl: './usr-form.component.html',
  styleUrls: ['./usr-form.component.css']
})
export class UsrFormComponent implements OnInit {
  private user:any = {}
  private salas = [];
  constructor(
    private salasService:SalasService,
    private usrService:UsrService
  ) { }

  ngOnInit() {
    this.salasService.getSalas()
    .map(res=> res.json())
    .subscribe((data)=>{
      this.salas = data
      console.log(this.salas);
    });
  }
  onSubmit(form){

  }

}

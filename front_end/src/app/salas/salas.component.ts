import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import 'rxjs/Rx';

import { SalasService } from './salas.service';
@Component({
  selector: 'app-salas',
  templateUrl: './salas.component.html',
  styleUrls: ['./salas.component.css']
})
export class SalasComponent implements OnInit {
  salasJson:any = [];
  
  constructor(
    private route:Router,
    private salasService:SalasService
  ) { }

  ngOnInit() {
    this.salasService
    .getSalas() 
    .map(res=> res.json())
    .subscribe((data)=>{
      this.salasJson = data
    });
  }
  editar(id){
    this.route.navigate(['/sala', id]);
  }
  deletarSala(id){
    this.salasService.deletarSala(id).subscribe();
  }
}

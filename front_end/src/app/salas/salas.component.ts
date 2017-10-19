import { DbService } from './../db-service.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import 'rxjs/Rx';

@Component({
  selector: 'app-salas',
  templateUrl: './salas.component.html',
  styleUrls: ['./salas.component.css']
})
export class SalasComponent implements OnInit {
  salasJson:any = [];
  
  constructor(
    private route:Router,
    private dbService:DbService
  ) { }

  ngOnInit() {
    this.dbService
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
    this.dbService.deletarSala(id).subscribe();
  }
}

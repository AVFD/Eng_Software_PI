import { DbService } from './../db.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-salas',
  templateUrl: './salas.component.html',
  styleUrls: ['./salas.component.css']
})
export class SalasComponent implements OnInit {
  salasJsonBackEnd:any = [];
  constructor(private dbService:DbService) { }

  ngOnInit() {
    this.dbService
    .getSalas() 
    .map(res=> res.json())
    .subscribe((data)=>{
      this.salasJsonBackEnd = data
    });
  }
  removeSala(id){
    this.dbService.removeSala(id).subscribe();
    this.ngOnInit();
    this.ngOnInit();
  }

}

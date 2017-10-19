import { DbService } from './../db-service.service';
import { Router } from '@angular/router';
import { getTestBed } from '@angular/core/testing';
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import 'rxjs/Rx';


@Component({
  selector: 'app-administrador',
  templateUrl: './administrador.component.html',
  styleUrls: ['./administrador.component.css']
})

export class AdministradorComponent implements OnInit {
  adminsJson:any = [];
  constructor(
    private route:Router, 
    private dbService: DbService,
  ) { }

  ngOnInit() {
    this.dbService
    .getAdministradores() 
    .map(res=> res.json())
    .subscribe((data)=>{
      this.adminsJson = data
    });
  }
  editar(id){
    this.route.navigate(['/admin', id]);
  }
  deletarAdm(id){
    this.dbService.deletarAdm(id).subscribe();
  }

}

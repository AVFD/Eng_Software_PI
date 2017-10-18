import { Router } from '@angular/router';
import { getTestBed } from '@angular/core/testing';
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import 'rxjs/Rx';

import { AdministradorService } from './administrador.service';

@Component({
  selector: 'app-administrador',
  templateUrl: './administrador.component.html',
  styleUrls: ['./administrador.component.css']
})

export class AdministradorComponent implements OnInit {
  adminsJson:any = [];
  constructor(
    private route:Router, 
    private administradorService:AdministradorService
  ) { }

  ngOnInit() {
    this.administradorService
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
    this.administradorService.deletarAdm(id).subscribe();
  }

}

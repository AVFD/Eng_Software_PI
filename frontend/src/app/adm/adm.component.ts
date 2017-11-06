import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { DbService } from './../db.service';

@Component({
  selector: 'app-adm',
  templateUrl: './adm.component.html',
  styleUrls: ['./adm.component.css']
})
export class AdmComponent implements OnInit {
  adminsJsonBackEnd:any = []
  constructor(
    private dbService: DbService,
    private router:Router
  ) { }

  ngOnInit() {
    this.dbService
    .getAdministradores() 
    .map(res=> res.json())
    .subscribe((data)=>{
      this.adminsJsonBackEnd = data
    });
  }
  deletarAdm(id){
    this.dbService.removeAdm(id).subscribe();
    this.ngOnInit();
    this.ngOnInit();
  }
  editar(id){
    this.router.navigate(['adm', id]);
  }
}

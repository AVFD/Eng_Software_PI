import { DbService } from './../../db.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-adm-edit',
  templateUrl: './adm-edit.component.html',
  styleUrls: ['./adm-edit.component.css']
})
export class AdmEditComponent implements OnInit {
  adminSelected:any = {
    'id': '',
    'name': '',
    'password': '',
    'email': ''
  };

  id: number;
  constructor(
    private routeActive: ActivatedRoute,
    private dbService: DbService,
    private router: Router
  ) { }

  ngOnInit() {
    this.routeActive.params.subscribe((params: any) => this.id = params['id']);
    this.dbService
      .getAdministrador(this.id)
      .map(res => res.json())
      .toPromise()
      .then((data) => {
        this.adminSelected = data.admins[0];
      })
  }
  onSubmit(form) {
    if(form.valid){
      this.dbService.updateAdministrador(this.adminSelected)
      .toPromise()
      .then(res => {
        alert('Administrador editado com sucesso!')
        this.router.navigate(['/adm'])
      })
      .catch(er => {
        this.errorMensage(er.status);
      });
    }
  }
  
  cancel() {
    this.router.navigate(['/adm'])
  }

  errorMensage(error){
    switch(error){
      case 409:{
        alert('Email já esta cadastrado!')
        break;
      }
    }
  }
}

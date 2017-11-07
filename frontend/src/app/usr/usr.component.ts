import { Router } from '@angular/router';
import { DbService } from './../db.service';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-usr',
  templateUrl: './usr.component.html',
  styleUrls: ['./usr.component.css']
})
export class UsrComponent implements OnInit {
  usrJsonBackEnd:any = [];

  constructor(
    private router:Router,
    private dbService:DbService
  ) { }

  ngOnInit() {
    this.dbService
    .getUsers()
    .map(res => res.json())
    .subscribe(data => {
      this.usrJsonBackEnd = data.users
    });
  }
  removeUser(id){
    this.dbService.removerUser(id).subscribe();
    this.ngOnInit();
    this.ngOnInit();
  }
  editar(id){
    this.router.navigate(['usr', id]);
  }
  
}

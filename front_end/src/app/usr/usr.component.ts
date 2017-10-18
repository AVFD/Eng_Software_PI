import { Component, OnInit } from '@angular/core';

import { UsrService } from './usr.service';
@Component({
  selector: 'app-usr',
  templateUrl: './usr.component.html',
  styleUrls: ['./usr.component.css']
})
export class UsrComponent implements OnInit {
  users = [];
  constructor(private usrService:UsrService) { }

  ngOnInit() {
    this.usrService.getUsers()
    .map(res=> res.json())
    .subscribe((data)=>{
      this.users = data;
    });
  }
  deletarUser(id){
    this.usrService.removerUser(id).subscribe();
  }

}

import { DbService } from './../db-service.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-usr',
  templateUrl: './usr.component.html',
  styleUrls: ['./usr.component.css']
})
export class UsrComponent implements OnInit {
  users = [];
  constructor(private dbService:DbService) { }

  ngOnInit() {
    this.dbService.getUsers()
    .map(res=> res.json())
    .subscribe((data)=>{
      this.users = data;
    });
  }
  deletarUser(id){
    this.dbService.removerUser(id).subscribe();
  }

}

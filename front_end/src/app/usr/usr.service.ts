import { Router } from '@angular/router';
import { Http } from '@angular/http';
import { Injectable } from '@angular/core';

const ip = "http://25.81.2.247:5000";
@Injectable()
export class UsrService {
  users = [];
  listarUsersURL = ip+"/user/read";
  removerUsersURL = ip+"/user/delete";
  constructor(
    private http:Http
  ) { }
  getUsers(){
    return this.http.get(this.listarUsersURL);
  }
  removerUser(id){
    return this.http.delete(this.removerUsersURL+"/"+id);

  }
}

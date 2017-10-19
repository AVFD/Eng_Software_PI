import { Http } from '@angular/http';
import { Injectable } from '@angular/core';


const ip = "http://127.0.0.1:5000";
@Injectable()
export class DbService {
  private criarSalaURL:string = ip+"/laboratory/create";
  private listaSalaURL:string = ip+"/laboratory/read";
  private deletarSalaURL:string = ip+"/laboratory/delete";
  private updateSalaURL:string = ip+"/laboratory/update";
  private listaradmURL:string = ip+"/admin/read";
  private criaradmURL:string = ip+"/admin/create";
  private deletaradmURL:string = ip+"/admin/delete";
  private updateadmURL:string = ip+"/admin/update";
  private listarUsersURL = ip+"/user/read";
  private removerUsersURL = ip+"/user/delete";
  constructor(private http:Http) { }
  //salas
  getSalas(){
    return this.http.get(this.listaSalaURL);
  }
  adicionarSala(salaJson){
    return this.http.post(this.criarSalaURL, salaJson);
  }
  deletarSala(id){
    return this.http.delete(this.deletarSalaURL+"/"+id);
  }
  getSala(id){
    return this.http.get(this.listaSalaURL+"/"+id);
  }
  updateSala(salaJson){
    return this.http.put(this.updateSalaURL,salaJson);
  }

  //adm
  getAdministradores(){
    return this.http.get(this.listaradmURL);
  }
  adicionarAdm(admin){
    return this.http.post(this.criaradmURL, admin);
  }
  deletarAdm(id){
    return this.http.delete(this.deletaradmURL+"/"+id);
  }
  getAdministrador(id){
    return this.http.get(this.listaradmURL+"/"+id);
  }
  updateAdministrador(admin){
    return this.http.put(this.updateadmURL,admin);
  }

  //users
  getUsers(){
    return this.http.get(this.listarUsersURL);
  }
  removerUser(id){
    return this.http.delete(this.removerUsersURL+"/"+id);
  }
}

import { Http } from '@angular/http';
import { Injectable } from '@angular/core';


const ip = "http://127.0.0.1:5000";
@Injectable()
export class DbService {
  private listarSalaURL:string = ip+"/laboratory/read";
  private criarSalaURL:string = ip+"/laboratory/create";
  private deletarSalaURL:string = ip+"/laboratory/delete";
  private updateSalaURL:string = ip+"/laboratory/update";

  private listarAdmURL:string = ip+"/admin/read";
  private criarAdmURL:string = ip+"/admin/create";
  private deletarAdmURL:string = ip+"/admin/delete";
  private updateAdmURL:string = ip+"/admin/update";

  private listarUsersURL:string = ip+"/user/read";
  private criarUserURL:string = ip+"/user/create";
  private deletarUserURL:string = ip+"/user/delete";
  private updateUserURL:string = ip+"/user/update";
  
  private criarScheduleURL:string = ip+"/schedule/create";
  private listarScheduleURL:string = ip+"/schedule/read";
  private deletarScheURL:string = ip+"/schedule/delete";
  private updateScheURL:string = ip+"/schedule/update";

  constructor(private http:Http) { }

  //salas
  getSalas(){
    return this.http.get(this.listarSalaURL);
  }
  getSala(id){
    return this.http.get(this.listarSalaURL+"/"+id);
  }
  adicionarSala(salaJson){
    return this.http.post(this.criarSalaURL, salaJson);
  }
  removerSala(id){
    return this.http.delete(this.deletarSalaURL+"/"+id);
  }
  updateSala(salaJson){
    return this.http.put(this.updateSalaURL,salaJson);
  }

  //adm
  getAdministradores(){
    return this.http.get(this.listarAdmURL);
  }
  getAdministrador(id){
    return this.http.get(this.listarAdmURL+"/"+id);
  }
  adicionarAdm(admin){
    return this.http.post(this.criarAdmURL, admin);
  }
  removerAdm(id){
    return this.http.delete(this.deletarAdmURL+"/"+id);
  }
  updateAdministrador(admin){
    return this.http.put(this.updateAdmURL,admin);
  }
  
  //users
  getUsers(){
    return this.http.get(this.listarUsersURL);
  }
  getUser(id){
    return this.http.get(this.listarUsersURL+"/"+id);
  }
  adicionarUser(user){
    return this.http.post(this.criarUserURL, user);
  }
  removerUser(id){
    return this.http.delete(this.deletarUserURL+"/"+id);
  }
  updateUser(user){
    return this.http.put(this.updateUserURL,user);
  }
  //Filtro User por profissao
  getFilterUser(opcao){
    return this.http.get(this.listarUsersURL+"?profession="+opcao)
  }

  //Schedule
  adicionarSchedule(schedule){
    return this.http.post(this.criarScheduleURL, schedule);
  }
  getScheduleByDay(dia, sala_id){
    return this.http.get(this.listarScheduleURL+"?day_of_the_week="+dia+"&laboratory_id="+sala_id);
  }
  removerSche(id){
    return this.http.delete(this.deletarScheURL+"/"+id);
  }
  getSchedule(id){
    return this.http.get(this.listarScheduleURL+"/"+id);
  }
  updateSchedule(schedule){
    return this.http.put(this.updateScheURL, schedule);
  }
}

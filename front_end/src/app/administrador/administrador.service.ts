import { Http } from '@angular/http';
import { Injectable } from '@angular/core';
import { Observable } from "rxjs/Observable";
const ip = "http://25.81.2.247:5000";
@Injectable()
export class AdministradorService {
  listaradmURL:string = ip+"/admin/read";
  criaradmURL:string = ip+"/admin/create";
  deletaradmURL:string = ip+"/admin/delete";
  updateadmURL:string = ip+"/admin/update";
  constructor(private http:Http) { }

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
}

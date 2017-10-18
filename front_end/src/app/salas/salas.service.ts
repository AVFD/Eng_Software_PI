import { Http } from '@angular/http';
import { Injectable } from '@angular/core';

const ip = "http://25.81.2.247:5000";
@Injectable()
export class SalasService {
  criarSalaURL:string = ip+"/laboratory/create";
  listaSalaURL:string = ip+"/laboratory/read";
  deletarSalaURL:string = ip+"/laboratory/delete";
  updateSalaURL:string = ip+"/laboratory/update";
  constructor(private http:Http) { }

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
}

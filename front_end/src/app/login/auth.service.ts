import { Injectable, EventEmitter} from '@angular/core';
import { Http } from '@angular/http';
import { Router } from '@angular/router';
import 'rxjs/add/operator/toPromise';

const ip = "http://25.81.2.247:5000";
@Injectable()
export class AuthService {
  private usuarioAutenticado:boolean = false;
  mostrarMenuEmitter = new EventEmitter<boolean>();
  url:string = ip+"/login";

  constructor(private http: Http)
  {}

  async fazerLogin(user){
    await this.http.post(this.url, user)
    .toPromise()
    .then(data => {
      if(data.status == 200){
        this.usuarioAutenticado = true;
        this.mostrarMenuEmitter.emit(true);
        return true;
      }
      this.usuarioAutenticado = false;
      this.mostrarMenuEmitter.emit(false);
      return false;
    })
    .catch((error)=> {
      this.usuarioAutenticado = false;
      this.mostrarMenuEmitter.emit(false);
      return false;
    });
    return this.usuarioAutenticado;
  }
  usuarioEstaAutenticado(){
    return this.usuarioAutenticado;
  }
}

import { Injectable, EventEmitter } from '@angular/core';
import { Http } from '@angular/http';
import { Router } from '@angular/router';
import 'rxjs/add/operator/toPromise';


const ip = "http://127.0.0.1:5000";
@Injectable()
export class AuthService {
  private usuarioAutenticado: boolean = false;
  url: string = ip + "/login";

  constructor(
    private http: Http,
  ) { }
  ngOnInit(){
   this.usuarioAutenticado = JSON.parse(localStorage.getItem('autenticado'));
   
  }
  async fazerLogin(user) {
    await this.http.post(this.url, user)
      .toPromise()
      .then(data => {
        if (data.status == 200) {
          localStorage.setItem('autentidado', 'true');
          this.usuarioAutenticado = true;
          return true;
        }
        this.usuarioAutenticado = false;
        localStorage.setItem('autentidado', 'false');
        return false;
      })
      .catch((error) => {
        console.log(error);
        this.errorMensage(error.status)
        return false;
      });
    return this.usuarioAutenticado;
  }
  usuarioEstaAutenticado() {
    return this.usuarioAutenticado;
  }
  setUsuarioEstaAutenticado(bool){
    this.usuarioAutenticado = bool;
  }
  errorMensage(error){
    switch(error){
      case 400:{
        alert('Login ou senha inválidos!')
        break;
      }
      case 404:{
        alert('Credenciais não cadastradas no sistema!')
      }
    }
  }
}

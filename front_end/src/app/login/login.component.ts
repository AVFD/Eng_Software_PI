import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Rx';

import { AuthService } from './auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  private usuarioJson = {  };

  constructor(private authService:AuthService, private route:Router) { }
  ngOnInit() {

  }

  async onSubmit(form){
    this.usuarioJson = {
      'username': form.value.nameuser,
      'password': form.value.password
    };
    await this.authService.fazerLogin(this.usuarioJson);
    
    if(this.authService.usuarioEstaAutenticado()){
      this.route.navigate(['/adm']);
    }
  }
}

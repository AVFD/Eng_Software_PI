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
  private usuarioJson = {};
  private errormensage: boolean = false;

  constructor(
    private authService: AuthService,
    private route: Router) { }
    
  ngOnInit() {

  }

  async onSubmit(form) {
    if (form.valid) {
      this.usuarioJson = {
        'username': form.value.username,
        'password': form.value.password
      };
      await this.authService.fazerLogin(this.usuarioJson);
      if(this.authService.usuarioEstaAutenticado){
        this.route.navigate(['/home']);
      }
    }
  }
}
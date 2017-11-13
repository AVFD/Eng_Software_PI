import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs/Observable';

import { AuthService } from './../login/auth.service';

@Injectable()
export class AuthGuard implements CanActivate{
  
    constructor(
      private authService:AuthService,
      private route:Router
    ) { }
    canActivate(
      route:ActivatedRouteSnapshot,
      state:RouterStateSnapshot
    ): Observable <boolean> | boolean {
      if(this.authService.usuarioEstaAutenticado()){
        return true;
      }else{
        this.route.navigate(['/']);
        return false;
      }
  
    }
  }
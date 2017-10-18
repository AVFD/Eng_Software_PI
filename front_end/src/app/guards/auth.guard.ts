import { Injectable} from '@angular/core';
import { Observable } from 'rxjs/Rx';
import { CanActivate,ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';

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
    }
    
    this.route.navigate(['/']);

    return false;
  }
}

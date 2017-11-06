import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AlertModule } from 'ngx-bootstrap';

import { routing } from './../app.routing';
import { NavbarComponent } from './navbar.component';

@NgModule({
  imports: [
    CommonModule,
    routing
  ],
  declarations: [
    NavbarComponent
  ],
  exports:[
    NavbarComponent
  ]
})
export class NavbarModule { }
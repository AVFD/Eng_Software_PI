import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { routing } from './../app.routing';
import { NavbarModule } from './../navbar/navbar.module';

import { SalasComponent } from './salas.component';
import { SalasFormComponent } from './salas-form/salas-form.component';
import { SalasEditComponent } from './salas-edit/salas-edit.component';

@NgModule({
  imports: [
    CommonModule,
    NavbarModule,
    FormsModule,
    routing,
    TooltipModule.forRoot()
  ],
  declarations: [
    SalasComponent,
    SalasFormComponent,
    SalasEditComponent
  ]
})
export class SalasModule { }

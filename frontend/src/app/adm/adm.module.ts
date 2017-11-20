import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TooltipModule } from 'ngx-bootstrap/tooltip';

import { NavbarModule } from './../navbar/navbar.module';
import { routing } from './../app.routing';

import { AdmComponent } from './adm.component';
import { AdmFormComponent } from './adm-form/adm-form.component';
import { AdmEditComponent } from './adm-edit/adm-edit.component';

@NgModule({
  imports: [
    CommonModule,
    NavbarModule,
    FormsModule,
    routing,
    TooltipModule.forRoot()
  ],
  declarations: [
    AdmComponent,
    AdmFormComponent,
    AdmEditComponent
  ]
})
export class AdmModule { }

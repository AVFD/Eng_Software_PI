import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NavbarModule } from './../navbar/navbar.module';
import { SalasComponent } from './salas.component';

@NgModule({
  imports: [
    CommonModule,
    NavbarModule,
    FormsModule
  ],
  declarations: [
    SalasComponent
  ]
})
export class SalasModule { }

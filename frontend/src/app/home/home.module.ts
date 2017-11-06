import { NavbarModule } from './../navbar/navbar.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeComponent } from './home.component';

@NgModule({
  imports: [
    CommonModule,
    NavbarModule
  ],
  declarations: [
    HomeComponent
  ]
})
export class HomeModule { }

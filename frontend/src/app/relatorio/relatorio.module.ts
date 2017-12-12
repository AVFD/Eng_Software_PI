import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { TextMaskModule } from 'angular2-text-mask';

import { NavbarModule } from './../navbar/navbar.module';

import { routing } from './../app.routing';

import { RelatorioComponent } from './relatorio.component';

@NgModule({
  imports: [
    CommonModule,
    routing,
    NavbarModule,
    FormsModule,
    TextMaskModule
  ],
  declarations: [RelatorioComponent]
})
export class RelatorioModule { }

import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { MultiselectDropdownModule } from 'angular-2-dropdown-multiselect';

import { UsrComponent } from './usr.component';
import { NavbarModule } from './../navbar/navbar.module';
import { UsrFormComponent } from './usr-form/usr-form.component';

import { routing } from './../app.routing';
import { UsrEditComponent } from './usr-edit/usr-edit.component';

@NgModule({
  imports: [
    CommonModule,
    NavbarModule,
    FormsModule,
    BsDropdownModule.forRoot(),
    routing,
    MultiselectDropdownModule,
    TooltipModule.forRoot()
  ],
  declarations: [
    UsrComponent,
    UsrFormComponent,
    UsrEditComponent
  ]
})
export class UsrModule { }

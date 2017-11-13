import { ScheduleComponent } from './schedule.component';
import { MultiselectDropdownModule } from 'angular-2-dropdown-multiselect';
import { routing } from './../app.routing';
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { FormsModule } from '@angular/forms';
import { NavbarModule } from './../navbar/navbar.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScheduleFormComponent } from './schedule-form/schedule-form.component';

@NgModule({
  imports: [
    CommonModule,
    NavbarModule,
    FormsModule,
    BsDropdownModule.forRoot(),
    routing,
    MultiselectDropdownModule
  ],
  declarations: [
    ScheduleComponent,
    ScheduleFormComponent
  ]
})
export class ScheduleModule { }

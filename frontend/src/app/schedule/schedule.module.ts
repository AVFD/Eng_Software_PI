import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { ScheduleComponent } from './schedule.component';
import { MultiselectDropdownModule } from 'angular-2-dropdown-multiselect';
import { routing } from './../app.routing';
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { FormsModule } from '@angular/forms';
import { NavbarModule } from './../navbar/navbar.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScheduleFormComponent } from './schedule-form/schedule-form.component';
import { ScheduleEditComponent } from './schedule-edit/schedule-edit.component';

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
    ScheduleComponent,
    ScheduleFormComponent,
    ScheduleEditComponent
  ]
})
export class ScheduleModule { }

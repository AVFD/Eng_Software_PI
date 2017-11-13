import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule }   from '@angular/forms';

import { AlertModule } from 'ngx-bootstrap';
import { MultiselectDropdownModule } from 'angular-2-dropdown-multiselect';
import { AngularMultiSelectModule } from 'angular2-multiselect-dropdown/angular2-multiselect-dropdown';

import { SalasModule } from './salas/salas.module';
import { ScheduleModule } from './schedule/schedule.module';
import { UsrModule } from './usr/usr.module';
import { PaginaoencotradaModule } from './paginaoencontrada/paginaoencotrada.module';
import { NavbarModule } from './navbar/navbar.module';
import { HomeModule } from './home/home.module';
import { LoginModule } from './login/login.module';
import { AdmModule } from './adm/adm.module';

import { AuthGuard } from './guards/auth.guard';
import { routing } from './app.routing';
import { AuthService } from './login/auth.service';
import { DbService } from './db.service';

import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AlertModule.forRoot(),
    MultiselectDropdownModule,
    AngularMultiSelectModule,
    LoginModule,
    HomeModule,
    AdmModule,
    UsrModule,
    SalasModule,
    NavbarModule,
    PaginaoencotradaModule,
    ScheduleModule,
    routing
  ],
  providers: [AuthGuard, AuthService, DbService],
  bootstrap: [AppComponent]
})
export class AppModule { }

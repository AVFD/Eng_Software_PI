import { UsrService } from './usr/usr.service';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AdministradorFormEditComponent } from './administrador-form-edit/administrador-form-edit.component';
import { SalasService } from './salas/salas.service';
import { AdministradorService } from './administrador/administrador.service';
import { AuthGuard } from './guards/auth.guard';
import { AppComponent } from './app.component';
import 'materialize-css';
import { MaterializeModule } from 'angular2-materialize';
import { LoginComponent } from './login/login.component';
import { AuthService } from './login/auth.service';
import { AppRoutingModule } from './app.routing.moduler';
import { AdministradorComponent } from './administrador/administrador.component';
import { UsrComponent } from './usr/usr.component';
import { PaginaNaoEncontradaComponent } from './pagina-nao-encontrada/pagina-nao-encontrada.component';
import { AdministradorFormComponent } from './administrador-form/administrador-form.component';
import { SalasComponent } from './salas/salas.component';
import { SalasFormComponent } from './salas-form/salas-form.component';
import { SalaFormEditComponent } from './sala-form-edit/sala-form-edit.component';
import { UsrFormComponent } from './usr-form/usr-form.component';
import { ErroComponent } from './erro/erro.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AdministradorComponent,
    UsrComponent,
    PaginaNaoEncontradaComponent,
    AdministradorFormComponent,
    SalasComponent,
    SalasFormComponent,
    AdministradorFormEditComponent,
    SalaFormEditComponent,
    UsrFormComponent,
    ErroComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterializeModule,
    AppRoutingModule
  ],
  providers: [AuthService, AuthGuard, AdministradorService, SalasService, UsrService],
  bootstrap: [AppComponent]
})
export class AppModule { }

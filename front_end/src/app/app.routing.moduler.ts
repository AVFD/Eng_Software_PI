import { UsrFormComponent } from './usr-form/usr-form.component';
import { SalaFormEditComponent } from './sala-form-edit/sala-form-edit.component';
import { NgModule, ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from "@angular/router";

import { ErroComponent } from './erro/erro.component'
import { AdministradorFormEditComponent } from './administrador-form-edit/administrador-form-edit.component';
import { SalasFormComponent } from './salas-form/salas-form.component';
import { SalasComponent } from './salas/salas.component';
import { AdministradorFormComponent } from './administrador-form/administrador-form.component';
import { PaginaNaoEncontradaComponent } from './pagina-nao-encontrada/pagina-nao-encontrada.component';
import { AuthGuard } from './guards/auth.guard';
import { UsrComponent } from './usr/usr.component';
import { LoginComponent } from './login/login.component';
import { AdministradorComponent } from './administrador/administrador.component';

const APP_ROUTES: Routes = [
    { path: 'adm', component: AdministradorComponent, canActivate:[AuthGuard]},
    { path: 'salas', component: SalasComponent, canActivate:[AuthGuard]},
    { path: 'usr', component: UsrComponent, canActivate:[AuthGuard]},
    { path: 'login', component: LoginComponent },
    { path: 'erro', component: ErroComponent },
    { path: 'sala/novo', component: SalasFormComponent, canActivate:[AuthGuard]},
    { path: 'user/novo', component: UsrFormComponent, canActivate:[AuthGuard]},
    { path: 'admin/novo', component: AdministradorFormComponent, canActivate:[AuthGuard]},
    { path: 'sala/:id', component: SalaFormEditComponent, canActivate:[AuthGuard]},
    { path: 'admin/:id', component: AdministradorFormEditComponent, canActivate:[AuthGuard]},
    { path: '', pathMatch: 'full', redirectTo: 'login' },
    { path: '**', component: PaginaNaoEncontradaComponent }

];

@NgModule({
    imports:[RouterModule.forRoot(APP_ROUTES)],
    exports:[RouterModule]
})
export class AppRoutingModule{}
import { ScheduleFormComponent } from './schedule/schedule-form/schedule-form.component';
import { ScheduleComponent } from './schedule/schedule.component';
import { SalasEditComponent } from './salas/salas-edit/salas-edit.component';
import { NgModule, ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from "@angular/router";

import { SalasFormComponent } from './salas/salas-form/salas-form.component';
import { UsrEditComponent } from './usr/usr-edit/usr-edit.component';
import { UsrFormComponent } from './usr/usr-form/usr-form.component';
import { AdmEditComponent } from './adm/adm-edit/adm-edit.component';
import { AdmFormComponent } from './adm/adm-form/adm-form.component';
import { UsrComponent } from './usr/usr.component';
import { SalasComponent } from './salas/salas.component';
import { AdmComponent } from './adm/adm.component';
import { PagiNaoEncontradaComponent } from './paginaoencontrada/paginaoencontrada.component';

import { HomeComponent } from './home/home.component';
import { AuthGuard } from './guards/auth.guard';
import { LoginComponent } from './login/login.component';

const APP_ROUTES: Routes = [
    { path: 'home', component: HomeComponent, canActivate:[AuthGuard]},
    { path: 'login', component: LoginComponent},
    { path: 'usr', component: UsrComponent, canActivate:[AuthGuard]},
    { path: 'salas', component: SalasComponent, canActivate:[AuthGuard]},
    { path: 'adm', component: AdmComponent, canActivate:[AuthGuard]},
    { path: 'schedule', component: ScheduleComponent, canActivate:[AuthGuard]},
    { path: 'salas/create', component: SalasFormComponent, canActivate:[AuthGuard]},
    { path: 'adm/create', component: AdmFormComponent, canActivate:[AuthGuard]},
    { path: 'usr/create', component: UsrFormComponent, canActivate:[AuthGuard]},
    { path: 'schedule/create', component: ScheduleFormComponent, canActivate:[AuthGuard]},
    { path: 'salas/:id', component: SalasEditComponent, canActivate:[AuthGuard]},
    { path: 'usr/:id', component: UsrEditComponent, canActivate:[AuthGuard]},
    { path: 'adm/:id', component: AdmEditComponent, canActivate:[AuthGuard]},
    { path: '', pathMatch: 'full', redirectTo: 'login' },
    { path: '**', component: PagiNaoEncontradaComponent }

];

export const routing: ModuleWithProviders = RouterModule.forRoot(APP_ROUTES);
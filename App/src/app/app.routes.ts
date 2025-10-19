import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { AdminComponent } from './pages/admin/admin.component';
import { MainPageComponent } from './pages/main-page/main-page.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'adminPage', component: AdminComponent },
  { path: 'mainPage', component: MainPageComponent },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];
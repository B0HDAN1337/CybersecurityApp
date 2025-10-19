import { Component, OnInit } from '@angular/core';
import { AuthService } from '../Services/auth.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  imports: [FormsModule, CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent implements OnInit {

  isLoggedIn = false;
  role: String | null = null;

   constructor(private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe(val => this.isLoggedIn = val);

    }
  

  signOut() {
    localStorage.removeItem('token');
    this.isLoggedIn = false;
    this.router.navigate(['/login']);
  }

  goToLogin() {
    this.router.navigate(['/login']);
  }

  goToRegister() {
    this.router.navigate(['/register']);
  }

}

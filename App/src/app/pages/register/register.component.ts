import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [FormsModule, HttpClientModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  firstname: string = '';
  lastname: string = '';
  email: string = '';
  password: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  register() {
    const body = { firstname: this.firstname, lastname: this.lastname, email: this.email, password: this.password };

    this.http.post<{ token: string }>('http://localhost:5152/api/User/Register', body).subscribe({
      next: (response) => {
        console.log("successful register");
        alert("Successful register");
      },
      error: (err) => {
        console.error('Register failed', err);
        alert('Email is already exists'); 
      }
    });
  }
}

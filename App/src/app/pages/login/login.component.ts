import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../Services/auth.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) {}

  login() {
    const body = { email: this.email, password: this.password };

    this.http.post<{ token: string }>('http://localhost:5152/api/User/login', body).subscribe({
      next: (response) => {
        const token = response.token;
        localStorage.setItem('token', token);

        const payload = JSON.parse(atob(token.split('.')[1]));
        const role = payload['http://schemas.microsoft.com/ws/2008/06/identity/claims/role'];
        
        console.log('Payload:', payload);
        console.log('Role:', role);


        if (role?.toLowerCase() === 'admin') {
          this.router.navigate(['/adminPage']);
        } else {
          this.router.navigate(['/mainPage']);
        }
          this.authService.login(token);

      },
      error: (err) => {
        console.error('Login failed', err);
        alert('Login failed. Check your credentials.');
      }
    });
  }
}

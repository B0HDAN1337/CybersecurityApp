import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loggedIn = new BehaviorSubject<boolean>(!!localStorage.getItem('token'));
  isLoggedIn$ = this.loggedIn.asObservable();

  login(token: string) {
    localStorage.setItem('token', token);
    this.loggedIn.next(true);
  }

  logout() {
    localStorage.removeItem('token');
    this.loggedIn.next(false);
  }
}
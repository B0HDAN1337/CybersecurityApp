import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  public isLoggedIn = new BehaviorSubject<boolean>(this.hasToken());

  constructor() { }

  private hasToken(): boolean {
    return !!localStorage.getItem('token');
  }

  login(token: string) {
    localStorage.setItem('token', token);
    this.isLoggedIn.next(true);
  }

  logout() {
    localStorage.removeItem('token');
    this.isLoggedIn.next(false);
  }

  getRole(): string | null {
    const token = localStorage.getItem('token');
    if (!token) return null;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload["http://schemas.microsoft.com/ws/2008/06/identity/claims/role"];
    } catch {
      return null;
    }
  }
}

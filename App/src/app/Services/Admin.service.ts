import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'http://localhost:5152/api/Admin';

  constructor(private http: HttpClient) {}

  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/AllUsers`);
  }

  updateUser(userId: number, data: Partial<User>) {
    return this.http.put(`${this.apiUrl}/UpdateUser/${userId}`, data);
  }

  deleteUser(userId: number) {
    return this.http.delete(`${this.apiUrl}/DeleteUser/${userId}`);
  }
}

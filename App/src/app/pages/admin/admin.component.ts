import { Component, OnInit } from '@angular/core';
import { User } from '../../models/user.model';
import { AdminService } from '../../Services/Admin.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule],
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.css'
})
export class AdminComponent implements OnInit {
  users: User[] = [];
  roles = ['Admin', 'User'];
  statuses = ['Active', 'Blocked'];
  passPolicies = ['true', 'false'];

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.adminService.getAllUsers().subscribe(users => {
      this.users = users;
    });
  }

  onRoleChange(user: User, event: any) {
    user.role = event.target.value;
    this.adminService.updateUser(user.id, { role: user.role }).subscribe();
  }

  onStatusChange(user: User, event: any) {
    user.status = event.target.value;
    this.adminService.updateUser(user.id, { status: user.status }).subscribe();
  }

  onPassPolicyChange(user: User, event: any) {
    user.passPolicy = event.target.value;
    this.adminService.updateUser(user.id, { passPolicy: user.passPolicy }).subscribe();
  }

  deleteUser(userId: number) {
    this.adminService.deleteUser(userId).subscribe(() => {
      this.users = this.users.filter(u => u.id !== userId);
    });
  }
}
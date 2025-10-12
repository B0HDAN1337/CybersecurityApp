using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace Server.Models
{

    public static class RoleUser
    {
        public const string Admin = "Admin";
        public const string User = "User";
    }

    public static class StatusUser
    {
        public const string Active = "Active";
        public const string Blocked = "Blocked";
    }

    public class User
    {
        public int Id { get; set; }
        public string Firstname { get; set; }
        public string Lastname { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
        public string Status { get; set; } = StatusUser.Active;
        public string Role { get; set; } = RoleUser.User;
    }
}
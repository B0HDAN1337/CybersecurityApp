using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace Server.ViewModel
{
    public class UserLoginViewModel
    {
        [Required]
        [EmailAddress(ErrorMessage = "Invalid email")]
        public string Email { get; set; }
        [Required]
        public string Password { get; set; }
    }
}
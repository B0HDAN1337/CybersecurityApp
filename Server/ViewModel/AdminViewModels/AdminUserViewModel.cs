using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Server.ViewModel.AdminViewModels
{
    public class AdminUserViewModel : UserViewModel
    {
        public string Role { get; set; }
        public string Status { get; set; }
    }
}
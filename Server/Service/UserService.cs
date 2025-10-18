using Server.Models;
using Server.Repository;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Microsoft.IdentityModel.Tokens;
using System.Text;
using Server.ViewModel;
using Server.ViewModel.AdminViewModels;
using System.Text.RegularExpressions;


namespace Server.Service
{
    public class UserService : IUserService
    {
        private readonly IUserRepository _repository;
        private readonly IHttpContextAccessor _httpContextAccessor;

        public UserService(IUserRepository repository, IHttpContextAccessor httpContextAccessor)
        {
            _repository = repository;
            _httpContextAccessor = httpContextAccessor;
        }

        public async Task<IEnumerable<User>> GetUserAllAsync()
        {
            var users = await _repository.GetAllAsync();

            return users;
        }

        public async Task<User> GetUserByIdAsync(int id)
        {
            return await _repository.GetByIdAsync(id);
        }

        public async Task<User> GetByEmailAsync(string email)
        {
            return await _repository.GetByEmailAsync(email);
        }

        public async Task<User> CreateUserAsync(object model)
        {
            var currentRole = _httpContextAccessor.HttpContext.User.FindFirstValue(ClaimTypes.Role);

            if (model is AdminUserViewModel adminModel && currentRole == RoleUser.Admin)
            {
                var adminUser = new User
                {
                    Firstname = adminModel.Firstname,
                    Lastname = adminModel.Lastname,
                    Email = adminModel.Email,
                    Password = BCrypt.Net.BCrypt.HashPassword(adminModel.Password, 13),
                    Role = adminModel.Role,
                    Status = adminModel.Status,
                    PasswordPolicy = adminModel.PasswordPolicy,
                    PasswordExpiresAt = adminModel.PasswordExpiresAt
                };

                return await _repository.CreateAsync(adminUser);

            }
            if (model is UserViewModel userModel)
            {
                var user = new User
                {
                    Firstname = userModel.Firstname,
                    Lastname = userModel.Lastname,
                    Email = userModel.Email,
                    Password = BCrypt.Net.BCrypt.HashPassword(userModel.Password, 13),
                    Role = RoleUser.User,
                    Status = StatusUser.Active
                };

                return await _repository.CreateAsync(user);
            }

            throw new UnauthorizedAccessException("You are not Authorized to create user");
        }

        public async Task<User> UpdateUserAsync(int id, object model)
        {
            var existUser = await _repository.GetByIdAsync(id);

            var currentRole = _httpContextAccessor.HttpContext.User.FindFirstValue(ClaimTypes.Role);

            if (existUser == null)
            {
                throw new Exception("User not found");
            }

            if (model is AdminUserViewModel adminModel && currentRole == RoleUser.Admin)
            {
                existUser.Firstname = adminModel.Firstname;
                existUser.Lastname = adminModel.Lastname;
                existUser.Email = adminModel.Email;
                existUser.Password = adminModel.Password;
                existUser.PasswordPolicy = adminModel.PasswordPolicy;
                existUser.PasswordExpiresAt = adminModel.PasswordExpiresAt;

                if (!string.IsNullOrWhiteSpace(adminModel.Password))
                {
                    existUser.Password = BCrypt.Net.BCrypt.HashPassword(adminModel.Password, 13);
                }

                return await _repository.UpdateAsync(id, existUser);
            }
            else if (currentRole == RoleUser.User && model is UserViewModel userModel)
            {
                existUser.Firstname = userModel.Firstname;
                existUser.Lastname = userModel.Lastname;
                existUser.Email = userModel.Email;
                existUser.Password = userModel.Password;

                if (existUser.PasswordPolicy)
                {
                    var pattern = @"^(?=.*[a-z])(?=.*[A-Z])(?=(?:.*\d){3,}).+$";
                    if (!Regex.IsMatch(userModel.Password, pattern))
                    {
                        throw new ArgumentException("The password must contain at least one uppercase letter, one lowercase letter, and three numbers.");
                    }
                }

                if (!string.IsNullOrWhiteSpace(userModel.Password))
                {
                    existUser.Password = BCrypt.Net.BCrypt.HashPassword(userModel.Password, 13);
                }

                return await _repository.UpdateAsync(id, existUser);
            }

             throw new UnauthorizedAccessException("You are not Authorized to create user");
        }

        public async Task<User> DeleteUserAsync(int id)
        {
            var deleteUser = await _repository.DeleteAsync(id);

            if (deleteUser == null)
            {
                throw new Exception("User not found");
            }

            return deleteUser;
        }

        public async Task<string> LoginUserAsync(string email, string password)
        {
            var userLogin = await _repository.LoginAsync(email);

            if (userLogin == null)
            {
                return null;
            }
            
            if(userLogin.Status == "Blocked")
            {
                return "Blocked";
            } else
            {
                bool isPasswordHash = BCrypt.Net.BCrypt.Verify(password, userLogin.Password);

            if (!isPasswordHash)
            {
                return null;
            }

            var claim = new[]
            {
                new Claim(ClaimTypes.NameIdentifier, userLogin.Id.ToString()),
                new Claim(ClaimTypes.Name, userLogin.Email),
                new Claim(ClaimTypes.Role, userLogin.Role)
            };

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("super_long_and_secure_key_at_least_32_bytes!"));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var token = new JwtSecurityToken(
                issuer: "App",
                audience: "App",
                claims: claim,
                expires: DateTime.Now.AddHours(1),
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
            }            
        }

        public int GetCurrentUserId()
        {
            var user = _httpContextAccessor.HttpContext.User;
            var claim = user.FindFirst(ClaimTypes.NameIdentifier);
            
            return int.Parse(claim.Value);
        }
    }
}
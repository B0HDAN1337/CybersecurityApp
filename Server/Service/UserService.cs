using Server.Models;
using Server.Repository;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Microsoft.IdentityModel.Tokens;
using System.Text;
using Server.ViewModel;


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

        public async Task<User> CreateUserAsync(UserViewModel viewModel)
        {
            var user = new User
            {
                Firstname = viewModel.Firstname,
                Lastname = viewModel.Lastname,
                Email = viewModel.Email,
                Password = BCrypt.Net.BCrypt.HashPassword(viewModel.Password, 13),
            };

            return await _repository.CreateAsync(user);
        }

        public async Task<User> UpdateUserAsync(int id, UserViewModel viewModel)
        {
            var existUser = await _repository.GetByIdAsync(id);

            if (existUser == null)
            {
                throw new Exception("User not found");
            }

            existUser.Email = viewModel.Email;

            if (!string.IsNullOrWhiteSpace(viewModel.Password))
            {
                existUser.Password = BCrypt.Net.BCrypt.HashPassword(viewModel.Password, 13);
            }

            return await _repository.UpdateAsync(id, existUser);
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

            bool isPasswordHash = BCrypt.Net.BCrypt.Verify(password, userLogin.Password);

            if (!isPasswordHash)
            {
                return null;
            }

            var claim = new[]
            {
                new Claim(ClaimTypes.NameIdentifier, userLogin.Id.ToString()),
                new Claim(ClaimTypes.Name, email),
                new Claim(ClaimTypes.Role, "User")
            };

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("keyGenerationTokenForUserIdentification"));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var token = new JwtSecurityToken(
                issuer: "IntelligentApp",
                audience: "IntelligentApp",
                claims: claim,
                expires: DateTime.Now.AddHours(1),
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public int GetCurrentUserId()
        {
            var user = _httpContextAccessor.HttpContext.User;
            var claim = user.FindFirst(ClaimTypes.NameIdentifier);
            
            return int.Parse(claim.Value);
        }
    }
}
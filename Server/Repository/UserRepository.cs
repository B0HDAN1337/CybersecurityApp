using Server.Data;
using Server.Models;
using Microsoft.EntityFrameworkCore;

namespace Server.Repository
{
    public class UserRepository : IUserRepository
    {
        private readonly AppDbContext _context;

        public UserRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<User>> GetAllAsync()
        {
            var users = await _context.Users.ToListAsync();

            return users;
        }

        public async Task<User> GetByIdAsync(int id)
        {
            var user = await _context.Users.FindAsync(id);

            return user;
        }

        public async Task<User> GetByEmailAsync(string email)
        {
            var user = await _context.Users.FirstOrDefaultAsync(u=> u.Email == email);
            
            return user;
        }

        public async Task<User> CreateAsync(User user)
        {
            var userExisting = await _context.Users.FirstOrDefaultAsync(u => u.Email == user.Email);

            if (userExisting != null)
            {
                throw new InvalidOperationException("User with this email is already exist");
            }

            await _context.Users.AddAsync(user);
            await _context.SaveChangesAsync();

            return user;
        }

        public async Task<User> UpdateAsync(int id, User user)
        {
            var existUser = await _context.Users.FindAsync(id);

            existUser.Firstname = user.Firstname;
            existUser.Lastname = user.Lastname;
            existUser.Email = user.Email;
            existUser.Password = user.Password;
            existUser.PasswordPolicy = user.PasswordPolicy;

            await _context.SaveChangesAsync();

            return existUser;
        }

        public async Task<User> DeleteAsync(int id)
        {
            var existRemove = await _context.Users.FindAsync(id);

            _context.Remove(existRemove);
            await _context.SaveChangesAsync();

            return existRemove;
        }

        public async Task<User> LoginAsync(string email)
        {
            var userLogin = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);

            if (userLogin == null)
            {
                return null;
            }

            return userLogin;
        }
    }
}
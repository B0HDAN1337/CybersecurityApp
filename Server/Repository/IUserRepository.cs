using Server.Models;

namespace Server.Repository
{
    public interface IUserRepository
    {
        Task<IEnumerable<User>> GetAllAsync();
        Task<User> GetByIdAsync(int id);
        Task<User> GetByEmailAsync(string email);
        Task<User> CreateAsync(User user);
        Task<User> UpdateAsync(int id, User user);
        Task<User> DeleteAsync(int id);
        Task<User> LoginAsync(string email);

    }
}
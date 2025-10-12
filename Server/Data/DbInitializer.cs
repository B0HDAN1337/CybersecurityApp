
namespace Server.Data
{
    public static class DbInitializer
    {
        public static void Initializer(AppDbContext context)
        {
            context.Database.EnsureCreated();
        }
    }
}

using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Repository;
using Server.Service;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.AspNetCore.Identity;
using Server.Models;
using System.Text;
using Microsoft.OpenApi.Models;
using Server.ViewModel;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddDbContext<AppDbContext>(options => options.UseNpgsql("Host=localhost;Database=App;Username=inteligentApp"));

// Repository
builder.Services.AddScoped<IUserRepository, UserRepository>();

// Service
builder.Services.AddScoped<IUserService, UserService>();

// http Accessor
builder.Services.AddHttpContextAccessor();


// JWT
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidIssuer = "App",
        ValidAudience = "App",
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("super_long_and_secure_key_at_least_32_bytes!"))
    };
});


builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    DbInitializer.Initializer(context);
}

// Seed Admin user
using (var scope = app.Services.CreateScope())
{
    var repo = scope.ServiceProvider.GetRequiredService<IUserRepository>();
    var admin = await repo.GetByEmailAsync("admin@system.com");
    if (admin == null)
    {
        await repo.CreateAsync(new User
        {
            Firstname = "System",
            Lastname = "Admin",
            Email = "admin@system.com",
            Password = BCrypt.Net.BCrypt.HashPassword("Admin123!"),
            Role = RoleUser.Admin,
            Status = StatusUser.Active
        });
    }
}

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();
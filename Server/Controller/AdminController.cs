using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Server.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using Server.Service;
using Server.ViewModel;

namespace Server.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class AdminController : ControllerBase
    {
        private readonly IUserService _service;
        public AdminController(IUserService service)
        {
            _service = service;
        }

        [HttpGet("AllUsers")]
        public async Task<IActionResult> GetAll()
        {
            var users = await _service.GetUserAllAsync();
            return Ok(users);
        }

        [HttpGet("User/{id}")]
        public async Task<IActionResult> GetById(int id)
        {
            var user = await _service.GetUserByIdAsync(id);
            return Ok(user);
        }

        [HttpPost("User/Create")]
        public async Task<IActionResult> Create([FromBody] UserViewModel userViewModel)
        {
            try
            {
                await _service.CreateUserAsync(userViewModel);
                return Ok();
            }
            catch (InvalidOperationException ex)
            {
                return BadRequest("User with this username or email is already exist");
            }
        }


        [HttpPut("UpdateUser/{id}")]
        public async Task<IActionResult> Update(int id, UserViewModel userViewModel)
        {
            await _service.UpdateUserAsync(id, userViewModel);
            return Ok();
        }


        [HttpDelete("DeleteUser/{id}")]
        public async Task<IActionResult> Delete(int id)
        {
            await _service.DeleteUserAsync(id);
            return Ok();
        }
        
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] UserLoginViewModel request)
        {
            var token = await _service.LoginUserAsync(request.Email, request.Password);
            if (token == null)
            {
                return Unauthorized();
            }

            return Ok(new { token });
        }
    }
}
using Microsoft.EntityFrameworkCore;
using PdvApi.Data;
using PdvApi.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new() { Title = "PDV API — Farmácia Boa Vista", Version = "v1" });
});

builder.Services.AddDbContext<PdvContext>(opt =>
    opt.UseInMemoryDatabase("pdv-dev"));

builder.Services.AddScoped<IVendaService, VendaService>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();

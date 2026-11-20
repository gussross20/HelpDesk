using HelpDesk.Application.Services;
using HelpDesk.Infrastructure;
using HelpDesk.Web.Components;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.AddScoped<ITicketService, TicketService>();

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

var app = builder.Build();

// MIGRACIÓN AUTOMÁTICA EN DESARROLLO
// TODO (Bloque 1 - 10:30 AM):
// Habilitar database.Migrate() al generar la migración InitialCreate con EF Core.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    app.UseHsts();
}

app.UseStatusCodePagesWithReExecute("/not-found", createScopeForStatusCodePages: true);
app.UseHttpsRedirection();

app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();

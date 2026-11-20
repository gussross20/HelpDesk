using HelpDesk.Domain.Interfaces;
using HelpDesk.Infrastructure.Persistence;
using HelpDesk.Infrastructure.Repositories;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace HelpDesk.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // TODO: Implementar en Capa Infrastructure
        var connectionString = configuration.GetConnectionString("DefaultConnection")
            ?? throw new InvalidOperationException("No se encontró la cadena de conexión 'DefaultConnection'.");

        services.AddDbContext<HelpDeskDbContext>(options =>
            options.UseSqlServer(connectionString));

        services.AddScoped<ICategoriaRepository, CategoriaRepository>();
        services.AddScoped<ITicketRepository, TicketRepository>();

        return services;
    }
}

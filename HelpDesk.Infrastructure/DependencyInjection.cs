using HelpDesk.Domain.Interfaces;
using HelpDesk.Infrastructure.Persistence;
using HelpDesk.Infrastructure.Repositories;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace HelpDesk.Infrastructure;

// Métodos de extensión para configurar y registrar los servicios de la capa de infraestructura
// en el contenedor de Inyección de Dependencias (IoC Container).
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var connectionString = configuration.GetConnectionString("DefaultConnection")
            ?? throw new InvalidOperationException("No se encontró la cadena de conexión 'DefaultConnection' en la configuración.");

        services.AddDbContext<HelpDeskDbContext>(options =>
            options.UseSqlServer(connectionString));

        services.AddScoped<ICategoriaRepository, CategoriaRepository>();
        services.AddScoped<ITicketRepository, TicketRepository>();

        return services;
    }
}

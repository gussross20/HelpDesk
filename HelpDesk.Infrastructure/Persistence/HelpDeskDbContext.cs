using HelpDesk.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace HelpDesk.Infrastructure.Persistence;

public class HelpDeskDbContext : DbContext
{
    public HelpDeskDbContext(DbContextOptions<HelpDeskDbContext> options) : base(options)
    {
    }

    public DbSet<Categoria> Categorias => Set<Categoria>();

    // TODO (Bloque 1 - 10:30 AM):
    // Descomentar y registrar los DbSets de Ticket y ComentarioTicket tras definir sus entidades:
    // public DbSet<Ticket> Tickets => Set<Ticket>();
    // public DbSet<ComentarioTicket> Comentarios => Set<ComentarioTicket>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Categoria>(entity =>
        {
            entity.ToTable("Categorias");
            entity.HasKey(c => c.Id);

            entity.Property(c => c.Nombre)
                .IsRequired()
                .HasMaxLength(100);

            entity.Property(c => c.Descripcion)
                .IsRequired()
                .HasMaxLength(250);

            // TODO (Bloque 1): Configurar relación 1:N Categoria -> Tickets
        });

        // TODO (Bloque 1 - 10:30 AM):
        // Configurar Fluent API para las entidades Ticket y ComentarioTicket:
        // - Claves primarias y longitudes máximas
        // - Relación 1:N Categoria -> Ticket (Restrict)
        // - Relación 1:N Ticket -> ComentarioTicket (Cascade)

        modelBuilder.Entity<Categoria>().HasData(
            new Categoria
            {
                Id = 1,
                Nombre = "Redes y Conectividad",
                Descripcion = "Problemas de Wi-Fi, cableado o acceso a internet"
            },
            new Categoria
            {
                Id = 2,
                Nombre = "Hardware y Periféricos",
                Descripcion = "Fallas en equipos de cómputo, monitores o impresoras"
            },
            new Categoria
            {
                Id = 3,
                Nombre = "Software y Licencias",
                Descripcion = "Instalación de programas, errores de sistema o licencias"
            },
            new Categoria
            {
                Id = 4,
                Nombre = "Cuentas y Accesos",
                Descripcion = "Restablecimiento de contraseñas y permisos institucionales"
            }
        );
    }
}

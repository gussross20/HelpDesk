using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Enums;
using Microsoft.EntityFrameworkCore;

namespace HelpDesk.Infrastructure.Persistence;

public class HelpDeskDbContext : DbContext
{
    public HelpDeskDbContext(DbContextOptions<HelpDeskDbContext> options) : base(options)
    {
    }

    public DbSet<Categoria> Categorias => Set<Categoria>();
    public DbSet<Ticket> Tickets => Set<Ticket>();
    public DbSet<ComentarioTicket> Comentarios => Set<ComentarioTicket>();

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

            entity.HasMany(c => c.Tickets)
                .WithOne(t => t.Categoria)
                .HasForeignKey(t => t.CategoriaId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        modelBuilder.Entity<Ticket>(entity =>
        {
            entity.ToTable("Tickets");
            entity.HasKey(t => t.Id);

            entity.Property(t => t.Titulo)
                .IsRequired()
                .HasMaxLength(150);

            entity.Property(t => t.Descripcion)
                .IsRequired()
                .HasMaxLength(1000);

            entity.Property(t => t.Prioridad)
                .IsRequired();

            entity.Property(t => t.Estado)
                .IsRequired();

            entity.Property(t => t.FechaCreacion)
                .IsRequired();

            entity.HasMany(t => t.Comentarios)
                .WithOne(c => c.Ticket)
                .HasForeignKey(c => c.TicketId)
                .OnDelete(DeleteBehavior.Cascade);
        });

        modelBuilder.Entity<ComentarioTicket>(entity =>
        {
            entity.ToTable("Comentarios");
            entity.HasKey(c => c.Id);

            entity.Property(c => c.Autor)
                .IsRequired()
                .HasMaxLength(100);

            entity.Property(c => c.Mensaje)
                .IsRequired()
                .HasMaxLength(500);

            entity.Property(c => c.Fecha)
                .IsRequired();
        });

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

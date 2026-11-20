using System;
using HelpDesk.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace HelpDesk.Infrastructure.Migrations
{
    [DbContext(typeof(HelpDeskDbContext))]
    [Migration("20261119063622_InitialCreate")]
    partial class InitialCreate
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "10.0.15")
                .HasAnnotation("Relational:MaxIdentifierLength", 128);

            SqlServerModelBuilderExtensions.UseIdentityColumns(modelBuilder);

            modelBuilder.Entity("HelpDesk.Domain.Entities.Categoria", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<string>("Descripcion")
                        .IsRequired()
                        .HasMaxLength(250)
                        .HasColumnType("nvarchar(250)");

                    b.Property<string>("Nombre")
                        .IsRequired()
                        .HasMaxLength(100)
                        .HasColumnType("nvarchar(100)");

                    b.HasKey("Id");

                    b.ToTable("Categorias", (string)null);

                    b.HasData(
                        new
                        {
                            Id = 1,
                            Descripcion = "Problemas de Wi-Fi, cableado o acceso a internet",
                            Nombre = "Redes y Conectividad"
                        },
                        new
                        {
                            Id = 2,
                            Descripcion = "Fallas en equipos de cómputo, monitores o impresoras",
                            Nombre = "Hardware y Periféricos"
                        },
                        new
                        {
                            Id = 3,
                            Descripcion = "Instalación de programas, errores de sistema o licencias",
                            Nombre = "Software y Licencias"
                        },
                        new
                        {
                            Id = 4,
                            Descripcion = "Restablecimiento de contraseñas y permisos institucionales",
                            Nombre = "Cuentas y Accesos"
                        });
                });

            modelBuilder.Entity("HelpDesk.Domain.Entities.ComentarioTicket", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<string>("Autor")
                        .IsRequired()
                        .HasMaxLength(100)
                        .HasColumnType("nvarchar(100)");

                    b.Property<DateTime>("Fecha")
                        .HasColumnType("datetime2");

                    b.Property<string>("Mensaje")
                        .IsRequired()
                        .HasMaxLength(500)
                        .HasColumnType("nvarchar(500)");

                    b.Property<int>("TicketId")
                        .HasColumnType("int");

                    b.HasKey("Id");

                    b.HasIndex("TicketId");

                    b.ToTable("Comentarios", (string)null);
                });

            modelBuilder.Entity("HelpDesk.Domain.Entities.Ticket", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<int>("CategoriaId")
                        .HasColumnType("int");

                    b.Property<string>("Descripcion")
                        .IsRequired()
                        .HasMaxLength(1000)
                        .HasColumnType("nvarchar(1000)");

                    b.Property<int>("Estado")
                        .HasColumnType("int");

                    b.Property<DateTime>("FechaCreacion")
                        .HasColumnType("datetime2");

                    b.Property<int>("Prioridad")
                        .HasColumnType("int");

                    b.Property<string>("Titulo")
                        .IsRequired()
                        .HasMaxLength(150)
                        .HasColumnType("nvarchar(150)");

                    b.HasKey("Id");

                    b.HasIndex("CategoriaId");

                    b.ToTable("Tickets", (string)null);
                });

            modelBuilder.Entity("HelpDesk.Domain.Entities.ComentarioTicket", b =>
                {
                    b.HasOne("HelpDesk.Domain.Entities.Ticket", "Ticket")
                        .WithMany("Comentarios")
                        .HasForeignKey("TicketId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Ticket");
                });

            modelBuilder.Entity("HelpDesk.Domain.Entities.Ticket", b =>
                {
                    b.HasOne("HelpDesk.Domain.Entities.Categoria", "Categoria")
                        .WithMany("Tickets")
                        .HasForeignKey("CategoriaId")
                        .OnDelete(DeleteBehavior.Restrict)
                        .IsRequired();

                    b.Navigation("Categoria");
                });

            modelBuilder.Entity("HelpDesk.Domain.Entities.Categoria", b =>
                {
                    b.Navigation("Tickets");
                });

            modelBuilder.Entity("HelpDesk.Domain.Entities.Ticket", b =>
                {
                    b.Navigation("Comentarios");
                });
#pragma warning restore 612, 618
        }
    }
}

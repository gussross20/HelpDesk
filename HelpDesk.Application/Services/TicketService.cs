using HelpDesk.Application.Common;
using HelpDesk.Application.DTOs;
using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Enums;
using HelpDesk.Domain.Interfaces;

// ARQUITECTURA: INVERSIÓN DE DEPENDENCIAS (DIP) Y DESACOPLAMIENTO DE INFRAESTRUCTURA
// Notice que en esta clase NO EXISTE 'using Microsoft.EntityFrameworkCore' ni 'using HelpDesk.Infrastructure'.
// La capa Application no conoce ni depende del motor de base de datos ni de EF Core.
// Solo interactúa con contratos de interfaz (ITicketRepository, ICategoriaRepository) definidos en Domain.
// ANTI-PATRÓN EVITADO: DEPENDENCY LEAK / VENDOR LOCK-IN
// Acoplar la lógica de negocio al ORM o base de datos específica imposibilita crear pruebas unitarias
// con mocks, dificulta migrar de motor o tecnología y rompe la regla de dependencia de Clean Architecture.

namespace HelpDesk.Application.Services;

public class TicketService : ITicketService
{
    private readonly ITicketRepository _ticketRepository;
    private readonly ICategoriaRepository _categoriaRepository;

    public TicketService(
        ITicketRepository ticketRepository,
        ICategoriaRepository categoriaRepository)
    {
        _ticketRepository = ticketRepository;
        _categoriaRepository = categoriaRepository;
    }

    public async Task<List<TicketResumenDto>> ObtenerTicketsAsync(EstadoTicket? estadoFiltro = null)
    {
        var tickets = await _ticketRepository.ObtenerTodosAsync(estadoFiltro);

        return tickets.Select(t => new TicketResumenDto
        {
            Id = t.Id,
            Titulo = t.Titulo,
            Prioridad = t.Prioridad,
            Estado = t.Estado,
            CategoriaNombre = t.Categoria?.Nombre ?? "Sin Asignar",
            FechaCreacion = t.FechaCreacion,
            TotalComentarios = t.Comentarios?.Count ?? 0
        }).ToList();
    }

    public async Task<Result<TicketDetalleDto>> ObtenerDetalleAsync(int id)
    {
        var ticket = await _ticketRepository.ObtenerPorIdConDetallesAsync(id);

        if (ticket is null)
        {
            // ARQUITECTURA: Uso del Patrón Result<T>.
            // ANTI-PATRÓN EVITADO: Control de flujo mediante excepciones ('throw new KeyNotFoundException').
            // Las excepciones degradan el rendimiento, alteran la pila de ejecución y ocultan resultados de negocio esperados.
            return Result<TicketDetalleDto>.Failure($"No se encontró el ticket con ID {id}.");
        }

        var detalleDto = new TicketDetalleDto
        {
            Id = ticket.Id,
            Titulo = ticket.Titulo,
            Descripcion = ticket.Descripcion,
            Prioridad = ticket.Prioridad,
            Estado = ticket.Estado,
            CategoriaNombre = ticket.Categoria?.Nombre ?? "Sin Asignar",
            FechaCreacion = ticket.FechaCreacion,
            Comentarios = ticket.Comentarios
                .OrderBy(c => c.Fecha) // Historial cronológico ascendente
                .Select(c => new ComentarioDto
                {
                    Id = c.Id,
                    Autor = c.Autor,
                    Mensaje = c.Mensaje,
                    Fecha = c.Fecha
                }).ToList()
        };

        return Result<TicketDetalleDto>.Success(detalleDto);
    }

    public async Task<Result<int>> CrearTicketAsync(CrearTicketDto dto)
    {
        if (dto.CategoriaId <= 0)
        {
            return Result<int>.Failure("Debe seleccionar una categoría válida.");
        }

        var ticket = new Ticket
        {
            Titulo = dto.Titulo.Trim(),
            Descripcion = dto.Descripcion.Trim(),
            Prioridad = dto.Prioridad,
            Estado = EstadoTicket.Abierto,
            FechaCreacion = DateTime.UtcNow,
            CategoriaId = dto.CategoriaId
        };

        await _ticketRepository.AgregarAsync(ticket);

        return Result<int>.Success(ticket.Id);
    }

    public async Task<Result> CambiarEstadoAsync(int id, EstadoTicket nuevoEstado)
    {
        var ticket = await _ticketRepository.ObtenerPorIdConDetallesAsync(id);

        if (ticket is null)
        {
            return Result.Failure($"No se encontró el ticket con ID {id}.");
        }

        // REGLA DE NEGOCIO OBLIGATORIA 2:
        // No se puede cambiar el estado de un ticket que ya está Resuelto a un estado anterior
        // (Abierto o EnProceso). Un ticket resuelto se considera archivado o finalizado.
        // ARQUITECTURA: Validación de invariantes de negocio dentro del servicio de aplicación.
        // ANTI-PATRÓN EVITADO: Anemic Domain / Bypass de Reglas en UI (la UI no debe ser la única que controle el flujo).
        if (ticket.Estado == EstadoTicket.Resuelto &&
           (nuevoEstado == EstadoTicket.Abierto || nuevoEstado == EstadoTicket.EnProceso))
        {
            return Result.Failure("No se puede cambiar el estado de un ticket que ya está Resuelto a un estado anterior (Abierto o En Proceso).");
        }

        ticket.Estado = nuevoEstado;
        await _ticketRepository.ActualizarAsync(ticket);

        return Result.Success();
    }

    public async Task<Result> AgregarComentarioAsync(AgregarComentarioDto dto)
    {
        var ticket = await _ticketRepository.ObtenerPorIdConDetallesAsync(dto.TicketId);

        if (ticket is null)
        {
            return Result.Failure($"No se encontró el ticket con ID {dto.TicketId}.");
        }

        if (ticket.Estado == EstadoTicket.Resuelto)
        {
            return Result.Failure("No se pueden agregar comentarios a un ticket que ya está Resuelto.");
        }

        var nuevoComentario = new ComentarioTicket
        {
            TicketId = dto.TicketId,
            Autor = dto.Autor.Trim(),
            Mensaje = dto.Mensaje.Trim(),
            Fecha = DateTime.UtcNow
        };

        await _ticketRepository.AgregarComentarioAsync(nuevoComentario);

        return Result.Success();
    }

    public async Task<List<Categoria>> ObtenerCategoriasAsync()
    {
        return await _categoriaRepository.ObtenerTodasAsync();
    }
}

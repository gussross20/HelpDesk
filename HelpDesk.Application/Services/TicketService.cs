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

    public Task<List<TicketResumenDto>> ObtenerTicketsAsync(EstadoTicket? estadoFiltro = null)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Consultar tickets a través de ITicketRepository y mapear a TicketResumenDto.
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task<Result<TicketDetalleDto>> ObtenerDetalleAsync(int id)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Consultar ticket por Id y devolver Result<TicketDetalleDto>.Success o Failure según corresponda.
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task<Result<int>> CrearTicketAsync(CrearTicketDto dto)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Validar DTO, instanciar entidad Ticket con Estado Inicial 'Abierto' y persistir.
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task<Result> CambiarEstadoAsync(int id, EstadoTicket nuevoEstado)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // REGLA DE NEGOCIO OBLIGATORIA 2:
        // No se puede cambiar el estado de un ticket que ya está Resuelto a un estado anterior
        // (Abierto o EnProceso). Devolver Result.Failure si se incumple la regla.
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task<Result> AgregarComentarioAsync(AgregarComentarioDto dto)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // REGLA DE NEGOCIO OBLIGATORIA 1:
        // No se puede agregar un comentario si el ticket tiene Estado == EstadoTicket.Resuelto.
        // Devolver Result.Failure si se incumple la regla.
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task<List<Categoria>> ObtenerCategoriasAsync()
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Consultar categorías desde ICategoriaRepository.
        throw new NotImplementedException("Implementar en el taller");
    }
}

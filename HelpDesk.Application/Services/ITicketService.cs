using HelpDesk.Application.Common;
using HelpDesk.Application.DTOs;
using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Enums;

namespace HelpDesk.Application.Services;

public interface ITicketService
{
    Task<List<TicketResumenDto>> ObtenerTicketsAsync(EstadoTicket? estadoFiltro = null);

    Task<Result<TicketDetalleDto>> ObtenerDetalleAsync(int id);

    Task<Result<int>> CrearTicketAsync(CrearTicketDto dto);

    Task<Result> CambiarEstadoAsync(int id, EstadoTicket nuevoEstado);

    Task<Result> AgregarComentarioAsync(AgregarComentarioDto dto);

    Task<List<Categoria>> ObtenerCategoriasAsync();
}

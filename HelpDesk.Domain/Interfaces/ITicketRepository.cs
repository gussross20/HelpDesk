using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Enums;

namespace HelpDesk.Domain.Interfaces;

public interface ITicketRepository
{
    Task<List<Ticket>> ObtenerTodosAsync(EstadoTicket? estadoFiltro = null);
    Task<Ticket?> ObtenerPorIdConDetallesAsync(int id);
    Task AgregarAsync(Ticket ticket);
    Task ActualizarAsync(Ticket ticket);
    Task AgregarComentarioAsync(ComentarioTicket comentario);
}

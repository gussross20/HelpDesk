using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Enums;
using HelpDesk.Domain.Interfaces;
using HelpDesk.Infrastructure.Persistence;

namespace HelpDesk.Infrastructure.Repositories;

// TODO: Implementar los 5 métodos (diapositiva 7).
public class TicketRepository : ITicketRepository
{
    private readonly HelpDeskDbContext _context;

    public TicketRepository(HelpDeskDbContext context)
    {
        _context = context;
    }

    public Task<List<Ticket>> ObtenerTodosAsync(EstadoTicket? estadoFiltro = null)
    {
        throw new NotImplementedException();
    }

    public Task<Ticket?> ObtenerPorIdConDetallesAsync(int id)
    {
        throw new NotImplementedException();
    }

    public Task AgregarAsync(Ticket ticket)
    {
        throw new NotImplementedException();
    }

    public Task ActualizarAsync(Ticket ticket)
    {
        throw new NotImplementedException();
    }

    public Task AgregarComentarioAsync(ComentarioTicket comentario)
    {
        throw new NotImplementedException();
    }
}

using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Enums;
using HelpDesk.Domain.Interfaces;
using HelpDesk.Infrastructure.Persistence;

namespace HelpDesk.Infrastructure.Repositories;

public class TicketRepository : ITicketRepository
{
    private readonly HelpDeskDbContext _context;

    public TicketRepository(HelpDeskDbContext context)
    {
        _context = context;
    }

    public Task<List<Ticket>> ObtenerTodosAsync(EstadoTicket? estadoFiltro = null)
    {
        // TODO: Implementar en Capa Infrastructure
        throw new NotImplementedException("TODO: Implementar en Capa Infrastructure");
    }

    public Task<Ticket?> ObtenerPorIdConDetallesAsync(int id)
    {
        // TODO: Implementar en Capa Infrastructure
        throw new NotImplementedException("TODO: Implementar en Capa Infrastructure");
    }

    public Task AgregarAsync(Ticket ticket)
    {
        // TODO: Implementar en Capa Infrastructure
        throw new NotImplementedException("TODO: Implementar en Capa Infrastructure");
    }

    public Task ActualizarAsync(Ticket ticket)
    {
        // TODO: Implementar en Capa Infrastructure
        throw new NotImplementedException("TODO: Implementar en Capa Infrastructure");
    }

    public Task AgregarComentarioAsync(ComentarioTicket comentario)
    {
        // TODO: Implementar en Capa Infrastructure
        throw new NotImplementedException("TODO: Implementar en Capa Infrastructure");
    }
}

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
        // TODO (Bloque 2 - 12:15 PM):
        // Implementar consulta de tickets con:
        // - AsNoTracking() para alto rendimiento en lecturas
        // - .Include(t => t.Categoria) y .Include(t => t.Comentarios) para evitar NullReferenceException
        // - Filtro opcional por estado
        // - Ordenamiento por FechaCreacion descendente
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task<Ticket?> ObtenerPorIdConDetallesAsync(int id)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Consultar ticket por Id incluyendo sus relaciones Categoria y Comentarios.
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task AgregarAsync(Ticket ticket)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Agregar ticket a la base de datos y llamar SaveChangesAsync().
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task ActualizarAsync(Ticket ticket)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Actualizar ticket en la base de datos y persistir cambios.
        throw new NotImplementedException("Implementar en el taller");
    }

    public Task AgregarComentarioAsync(ComentarioTicket comentario)
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Agregar comentario y persistir cambios.
        throw new NotImplementedException("Implementar en el taller");
    }
}

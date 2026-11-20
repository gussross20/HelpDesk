using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Enums;
using HelpDesk.Domain.Interfaces;
using HelpDesk.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HelpDesk.Infrastructure.Repositories;

public class TicketRepository : ITicketRepository
{
    private readonly HelpDeskDbContext _context;

    public TicketRepository(HelpDeskDbContext context)
    {
        _context = context;
    }

    public async Task<List<Ticket>> ObtenerTodosAsync(EstadoTicket? estadoFiltro = null)
    {
        // ARQUITECTURA: Eager Loading con .Include(t => t.Categoria) y .Include(t => t.Comentarios)
        // EF Core traduce esto a operaciones JOIN optimizadas en SQL Server, cargando en memoria
        // las entidades relacionadas necesarias para mapear los DTOs en una sola consulta.
        // ANTI-PATRÓN EVITADO: NULL REFERENCE EXCEPTION & N+1 QUERIES
        // Sin .Include(), las propiedades de navegación 'Categoria' y 'Comentarios' permanecen nulas (null),
        // provocando NullReferenceException al intentar acceder a 't.Categoria.Nombre' o 't.Comentarios.Count'.
        // Además, evita el anti-patrón de consultas N+1 donde cada ticket dispara una consulta extra a la BD.
        var query = _context.Tickets
            .AsNoTracking()
            .Include(t => t.Categoria)
            .Include(t => t.Comentarios)
            .AsQueryable();

        if (estadoFiltro.HasValue)
        {
            query = query.Where(t => t.Estado == estadoFiltro.Value);
        }

        return await query
            .OrderByDescending(t => t.FechaCreacion)
            .ToListAsync();
    }

    public async Task<Ticket?> ObtenerPorIdConDetallesAsync(int id)
    {
        // ARQUITECTURA: Carga explícita y completa del agregado Ticket con sus relaciones.
        // ANTI-PATRÓN EVITADO: NullReferenceException al acceder al historial de comentarios o nombre de categoría en vistas de detalle.
        return await _context.Tickets
            .Include(t => t.Categoria)
            .Include(t => t.Comentarios)
            .FirstOrDefaultAsync(t => t.Id == id);
    }

    public async Task AgregarAsync(Ticket ticket)
    {
        await _context.Tickets.AddAsync(ticket);
        await _context.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Ticket ticket)
    {
        if (_context.Entry(ticket).State == EntityState.Detached)
        {
            _context.Tickets.Update(ticket);
        }

        await _context.SaveChangesAsync();
    }

    public async Task AgregarComentarioAsync(ComentarioTicket comentario)
    {
        await _context.Comentarios.AddAsync(comentario);
        await _context.SaveChangesAsync();
    }
}

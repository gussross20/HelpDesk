using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Interfaces;
using HelpDesk.Infrastructure.Persistence;

namespace HelpDesk.Infrastructure.Repositories;

public class CategoriaRepository : ICategoriaRepository
{
    private readonly HelpDeskDbContext _context;

    public CategoriaRepository(HelpDeskDbContext context)
    {
        _context = context;
    }

    public Task<List<Categoria>> ObtenerTodasAsync()
    {
        // TODO (Bloque 2 - 12:15 PM):
        // Implementar consulta de categorías utilizando EF Core (_context.Categorias.AsNoTracking().ToListAsync())
        throw new NotImplementedException("Implementar en el taller");
    }
}

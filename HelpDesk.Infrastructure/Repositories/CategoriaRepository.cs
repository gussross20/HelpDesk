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

    // TODO: Consulta de categorías (diapositiva 7).
    public Task<List<Categoria>> ObtenerTodasAsync()
    {
        throw new NotImplementedException();
    }
}

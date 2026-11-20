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
        // TODO: Implementar en Capa Infrastructure
        throw new NotImplementedException("TODO: Implementar en Capa Infrastructure");
    }
}

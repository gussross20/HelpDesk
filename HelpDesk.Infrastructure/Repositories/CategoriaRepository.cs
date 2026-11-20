using HelpDesk.Domain.Entities;
using HelpDesk.Domain.Interfaces;
using HelpDesk.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace HelpDesk.Infrastructure.Repositories;

public class CategoriaRepository : ICategoriaRepository
{
    private readonly HelpDeskDbContext _context;

    public CategoriaRepository(HelpDeskDbContext context)
    {
        _context = context;
    }

    public async Task<List<Categoria>> ObtenerTodasAsync()
    {
        return await _context.Categorias
            .AsNoTracking()
            .OrderBy(c => c.Nombre)
            .ToListAsync();
    }
}

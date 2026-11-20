using HelpDesk.Domain.Entities;

namespace HelpDesk.Domain.Interfaces;

public interface ICategoriaRepository
{
    Task<List<Categoria>> ObtenerTodasAsync();
}

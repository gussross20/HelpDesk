using HelpDesk.Domain.Enums;

namespace HelpDesk.Domain.Entities;

public class Ticket
{
    public int Id { get; set; }
    public string Titulo { get; set; } = string.Empty;
    public string Descripcion { get; set; } = string.Empty;
    public PrioridadTicket Prioridad { get; set; } = PrioridadTicket.Media;
    public EstadoTicket Estado { get; set; } = EstadoTicket.Abierto;
    public DateTime FechaCreacion { get; set; } = DateTime.UtcNow;

    public int CategoriaId { get; set; }
    public Categoria Categoria { get; set; } = null!;

    public ICollection<ComentarioTicket> Comentarios { get; set; } = new List<ComentarioTicket>();
}

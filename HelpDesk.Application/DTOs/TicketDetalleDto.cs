using HelpDesk.Domain.Enums;

namespace HelpDesk.Application.DTOs;

public class TicketDetalleDto
{
    public int Id { get; set; }
    public string Titulo { get; set; } = string.Empty;
    public string Descripcion { get; set; } = string.Empty;
    public PrioridadTicket Prioridad { get; set; }
    public EstadoTicket Estado { get; set; }
    public string CategoriaNombre { get; set; } = string.Empty;
    public DateTime FechaCreacion { get; set; }
    public List<ComentarioDto> Comentarios { get; set; } = new();
}

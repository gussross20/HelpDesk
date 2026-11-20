using HelpDesk.Domain.Enums;

namespace HelpDesk.Application.DTOs;

public class TicketResumenDto
{
    public int Id { get; set; }
    public string Titulo { get; set; } = string.Empty;
    public PrioridadTicket Prioridad { get; set; }
    public EstadoTicket Estado { get; set; }
    public string CategoriaNombre { get; set; } = string.Empty;
    public DateTime FechaCreacion { get; set; }
    public int TotalComentarios { get; set; }
}

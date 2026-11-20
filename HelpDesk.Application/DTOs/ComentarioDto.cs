namespace HelpDesk.Application.DTOs;

public class ComentarioDto
{
    public int Id { get; set; }
    public string Autor { get; set; } = string.Empty;
    public string Mensaje { get; set; } = string.Empty;
    public DateTime Fecha { get; set; }
}

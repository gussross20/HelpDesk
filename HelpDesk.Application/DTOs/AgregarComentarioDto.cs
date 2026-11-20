using System.ComponentModel.DataAnnotations;

namespace HelpDesk.Application.DTOs;

public class AgregarComentarioDto
{
    public int TicketId { get; set; }

    [Required(ErrorMessage = "El nombre del autor es obligatorio.")]
    [StringLength(100, ErrorMessage = "El autor no puede superar los 100 caracteres.")]
    public string Autor { get; set; } = string.Empty;

    [Required(ErrorMessage = "El mensaje del comentario no puede estar vacío.")]
    [StringLength(500, ErrorMessage = "El comentario no puede superar los 500 caracteres.")]
    public string Mensaje { get; set; } = string.Empty;
}

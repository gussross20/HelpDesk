using System.ComponentModel.DataAnnotations;
using HelpDesk.Domain.Enums;

namespace HelpDesk.Application.DTOs;

// ARQUITECTURA: PATRÓN DTO (DATA TRANSFER OBJECT)
// Define un contrato estricto con los datos exactos requeridos por la vista para crear un ticket.
// Aísla el modelo de dominio de los datos provenientes de la capa de presentación (Blazor UI / HTTP).
// ANTI-PATRÓN EVITADO: OVERPOSTING / MASS ASSIGNMENT VULNERABILITY
// Si un formulario web enlaza directamente a la entidad de dominio 'Ticket', un usuario
// malintencionado podría enviar datos no deseados e inyectar valores en propiedades como 'Id',
// 'FechaCreacion' o alterar 'Estado' directamente a 'Resuelto' saltándose el ciclo de vida del negocio.
// El DTO solo expone los campos que el usuario tiene permitido ingresar.
public class CrearTicketDto
{
    [Required(ErrorMessage = "El título del ticket es obligatorio.")]
    [StringLength(150, ErrorMessage = "El título no puede exceder los 150 caracteres.")]
    public string Titulo { get; set; } = string.Empty;

    [Required(ErrorMessage = "La descripción del problema es obligatoria.")]
    [StringLength(1000, ErrorMessage = "La descripción no puede exceder los 1000 caracteres.")]
    public string Descripcion { get; set; } = string.Empty;

    [Required(ErrorMessage = "Debe asignar una prioridad al ticket.")]
    public PrioridadTicket Prioridad { get; set; } = PrioridadTicket.Media;

    [Range(1, int.MaxValue, ErrorMessage = "Seleccione una categoría válida.")]
    public int CategoriaId { get; set; }
}

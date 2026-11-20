# 🛠️ HelpDesk - Taller Universitario de Clean Architecture y Patrones de Diseño

Bienvenido al repositorio del taller práctico de **Clean Architecture y Patrones de Diseño en .NET 10** utilizando **Blazor Web App (Interactive Server)** y **SQL Server con Entity Framework Core**.

Este proyecto está diseñado didácticamente como una guía progresiva mediante ramas de Git. Los estudiantes pueden iniciar desde un *Starter Kit* funcional y avanzar bloque por bloque construyendo una arquitectura limpia, desacoplada y basada en buenas prácticas de la industria.

---

## 🏛️ Diagrama de Arquitectura (Clean Architecture Pragmática)

La regla de oro de Clean Architecture establece que **las dependencias solo apuntan hacia adentro**:

```
+---------------------------------------------------------------------------------+
|                                  HelpDesk.Web                                   |
|                      (Blazor Interactive Server + Bootstrap 5)                  |
+---------------------------------------+-----------------------------------------+
                                        |
                 Referencia a           |          Referencia a
                 Application            |          Infrastructure (para DI)
                                        v
+---------------------------------------+-----------------------------------------+
|                              HelpDesk.Application                               |
|        (Casos de Uso, Servicios, DTOs, Validaciones, Patrón Result)             |
+---------------------------------------+-----------------------------------------+
                                        |
                 Referencia a           |
                 Domain                 |
                                        v
+---------------------------------------+-----------------------------------------+
|                                HelpDesk.Domain                                  |
|         (Entidades de Negocio, Enums, Interfaces de Repositorios - C# Puro)     |
+---------------------------------------+-----------------------------------------+
                                        ^
                 Implementa interfaces  |
                 definidas en Domain    |
+---------------------------------------+-----------------------------------------+
|                            HelpDesk.Infrastructure                              |
|           (EF Core, SQL Server, Mapeos Fluent API, Repositorios Concretos)      |
+---------------------------------------------------------------------------------+
```

### Principios Clave Aplicados:
1. **HelpDesk.Domain:** No depende de ningún otro proyecto ni de paquetes NuGet externos. C# puro.
2. **HelpDesk.Application:** Depende únicamente de `HelpDesk.Domain`. No tiene referencias a Entity Framework Core ni SQL Server (Inversión de Dependencias - DIP).
3. **HelpDesk.Infrastructure:** Depende de `HelpDesk.Domain` e implementa los contratos de repositorio (`ITicketRepository`, `ICategoriaRepository`).
4. **HelpDesk.Web:** Orquesta la interfaz con Blazor Interactive Server. Solo inyecta `ITicketService` en sus componentes visuales, evitando la fuga de abstracción de la base de datos hacia la UI.

---

## 🗺️ Mapa de Ramas y Checkpoints del Taller

Cada rama representa un hito progresivo del taller. Todas las ramas compilan limpiamente con `dotnet build`:

| Rama | Horario / Bloque | Objetivo y Conceptos Aprendidos |
|---|---|---|
| `main` | 09:00 AM (Inicio) | **Starter Kit:** Estructura de proyectos, referencias, DTOs, Enums y entidad `Categoria` de ejemplo. Métodos vacíos con `TODO:` y `NotImplementedException`. |
| `01-dominio-y-datos` | 10:30 AM (Fin Bloque 1) | **Dominio y Persistencia:** Entidades `Ticket` y `ComentarioTicket`, relaciones 1:N con Fluent API en `HelpDeskDbContext`, Data Seeding y creación de la migración `InitialCreate`. |
| `02-repositorios-y-servicios` | 12:15 PM (Fin Bloque 2) | **Lógica de Negocio y Repositorios:** Implementación del patrón Repositorio (con `.Include()`), `TicketService` con reglas de transición de estado y adopción del `Result Pattern` en lugar de excepciones. |
| `03-ui-tablero-y-creacion` | 01:30 PM (Fin Bloque 3) | **Interfaz Reactiva Blazor:** Registro de DI en `Program.cs`, pantalla de listado (`/tickets`) con métricas y formulario de creación (`/tickets/nuevo`) con `EditForm` y validaciones DataAnnotations. |
| `final` | Versión Completa | **Solución Integral Terminada:** Incluye la pantalla de detalle (`/tickets/{Id}`) con gestión de estados, bloqueo por regla de negocio e historial cronológico de comentarios. |

---

## ⚡ Comandos Rápidos

### 1. Clonar y Navegar entre Ramas

Para moverte al checkpoint que desees explorar:
```bash
# Ver todas las ramas disponibles
git branch -a

# Ir al Starter Kit inicial (9:00 AM)
git checkout main

# Ver el avance al final del Bloque 1
git checkout 01-dominio-y-datos

# Ver el avance al final del Bloque 2
git checkout 02-repositorios-y-servicios

# Ver el avance al final del Bloque 3
git checkout 03-ui-tablero-y-creacion

# Ver la versión final 100% terminada
git checkout final
```

### 2. Comparar el Avance entre Bloques

Puedes ver exactamente qué código se implementó en cada bloque con `git diff`:
```bash
# Ver cambios implementados durante el Bloque 1
git diff main..01-dominio-y-datos

# Ver cambios implementados durante el Bloque 2
git diff 01-dominio-y-datos..02-repositorios-y-servicios

# Ver cambios implementados durante el Bloque 3
git diff 02-repositorios-y-servicios..03-ui-tablero-y-creacion

# Ver el reto final implementado
git diff 03-ui-tablero-y-creacion..final
```

### 3. Compilación y Restauración de Base de Datos

```bash
# Compilar la solución completa
dotnet build HelpDesk.sln

# Aplicar migraciones a SQL Server (crea la BD 'HelpDeskTallerDb' y carga datos semilla)
dotnet ef database update --project HelpDesk.Infrastructure --startup-project HelpDesk.Web

# Ejecutar la aplicación web Blazor
dotnet run --project HelpDesk.Web --launch-profile http
```

La aplicación estará accesible en: `http://localhost:5237`

---

## 📚 Anti-Patrones Explicados en el Código

En el código fuente encontrarás comentarios especiales `// ARQUITECTURA:` y `// ANTI-PATRÓN EVITADO:` que explican decisiones de diseño cruciales:
- **`TicketService.cs`:** Explica por qué no existe `using Microsoft.EntityFrameworkCore` (Inversión de Dependencias) y por qué se usa `Result<T>` en vez de lanzar excepciones para flujos de negocio.
- **`TicketRepository.cs`:** Explica el uso de `.Include()` para evitar errores de referencia nula (NullReferenceException) y el anti-patrón de consultas N+1.
- **`CrearTicketDto.cs`:** Explica cómo el patrón DTO previene vulnerabilidades de asignación masiva (*Overposting*).
- **`Tickets.razor`:** Explica por qué la interfaz de usuario jamás inyecta el `DbContext` directamente (*Smart UI Anti-Pattern*).

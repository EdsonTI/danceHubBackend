---
description: Instrucciones estrictas para modelos de BD y la arquitectura de Identidad JSONB.
applyTo: ['app/models/**/*.py', 'migrations/**/*.py']
---

# Rol: Database Architect (Alembic & SQLAlchemy 2.0)

## Reglas de Modelado de Datos
1. **Sintaxis SQLAlchemy 2.0:** Usa `Mapped[]` y `mapped_column()`.
2. **Arquitectura de Identidad (Global vs Local):**
   - **`User`**: Entidad base humana (email, nombre). SIN school_id.
   - **`Role`**: Catálogo de roles.
   - **`UserProfile`**: Entidad GLOBAL que vincula `User` + `Role`. Contiene la columna `extra_details` de tipo `JSONB` (PostgreSQL) para guardar datos dinámicos del perfil (ej. bio de profesor, o lesiones de alumno). SIN school_id.
   - **`RoleAssignment`**: Entidad LOCAL que vincula `User` + `Role` + `School`. Obligatorio `school_id`.
3. **Columnas JSON:** Cuando uses JSON, importa `JSONB` del dialecto de PostgreSQL (`from sqlalchemy.dialects.postgresql import JSONB`).
4. **Prohibición:** NUNCA sugieras `db.create_all()`. Todo cambio es migración de Alembic.
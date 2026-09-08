---
description: Contexto global del proyecto DanceHub (Marketplace + SaaS) y reglas arquitectónicas principales.
applyTo: '**/*.py'
---

# Contexto del Proyecto: DanceHub Backend

Eres un Senior Software Engineer experto en Python. Trabajas en "DanceHub", una plataforma híbrida (Marketplace B2B2C + SaaS) para escuelas de baile, similar a Mindbody.

## Stack Tecnológico
- Framework: FastAPI
- ORM: SQLAlchemy 2.0 (sintaxis declarativa moderna)
- Base de Datos: PostgreSQL
- Validaciones: Pydantic v2
- Migraciones: Alembic
- Auth: JWT (JSON Web Tokens) con Scoped Contexts

## Arquitectura de Negocio Crítica
1. **Entidades Globales vs Locales:**
   - **Globales:** Identidades como `User`, `StudentProfile` y `TeacherProfile` NO pertenecen a una escuela (no tienen `school_id`).
   - **Locales:** Entidades operativas como `DanceClass`, `Schedule` o `Transactions` SÍ pertenecen a una escuela (llevan `school_id`).
   - **Asignaciones:** La relación entre usuarios globales y escuelas se da mediante tablas de intersección (`RoleAssignment`, `ClassEnrollment`).
2. **Context Switching (Multi-Rol):** Un usuario puede ser alumno en la Escuela A y profesor en la Escuela B. La API debe operar basándose en un JWT que defina el "Contexto Activo" (tenant y rol actual).
3. **Descubrimiento (Marketplace):** Escuelas y clases tienen banderas de visibilidad (`is_public`, `visibility='PUBLIC'|'INTERNAL'`).
4. **Monetización Freemium:** El sistema cuenta "Alumnos Activos" y maneja planes de facturación (SaaS fijo o Comisión por transacción).
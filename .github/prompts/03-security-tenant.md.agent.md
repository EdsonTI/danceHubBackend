---
description: Instrucciones para implementar Scoped JWTs, validaciones de multi-rol, y aislamiento de transacciones.
applyTo: ['app/core/security.py', 'app/api/dependencies.py', 'app/services/**/*.py']
---

# Rol: Security & Auth Engineer

## Objetivo
Garantizar el aislamiento de datos (Tenant Isolation) y gestionar el "Context Switching" de los usuarios.

## Reglas de Implementación
1. **Scoped Tokens:** El JWT no es estático. Cuando un usuario opera dentro de una escuela, el cliente envía un JWT que contiene los claims `active_school_id` y `active_role`.
2. **Verificación de Seguridad:** La dependencia de FastAPI (ej. `get_current_tenant_context()`) debe leer el token, rechazar el acceso si expira, y prohibir que un usuario con `active_role='STUDENT'` acceda a endpoints donde se requiere `SCHOOL_ADMIN`.
3. **Inyección de ID Inquebrantable:** En operaciones POST/PUT dentro de `/api/tenant/`, el `school_id` jamás se lee del payload JSON. Se inyecta forzosamente en el servicio usando el `active_school_id` extraído del token verificado.
---
description: Instrucciones para el diseño de endpoints, división entre API de Tenant y API de Marketplace, y esquemas Pydantic.
applyTo: ['app/api/**/*.py', 'app/schemas/**/*.py']
---

# Rol: API Developer (FastAPI & Pydantic v2)

## Objetivo
Construir la capa de transporte dividiendo el acceso interno de las escuelas y la exposición pública del marketplace.

## Reglas de Implementación
1. **Estructura de Endpoints (Dos Mundos):**
   - Rutas `/api/tenant/...`: Requieren JWT con el contexto activo de la escuela. Las consultas aquí inyectan el `school_id` automáticamente en el `WHERE`.
   - Rutas `/api/discover/...`: Rutas del Marketplace. Las consultas aquí cruzan múltiples escuelas pero EXIGEN el filtro `is_public == True` y `visibility == 'PUBLIC'`.
2. **Patrón de Schemas (Pydantic v2):** 
   - Genera siempre `{Entity}Base`, `{Entity}Create` (sin ID) y `{Entity}Response` (con ID y `model_config = ConfigDict(from_attributes=True)`).
3. **Controladores Limpios:** El router de FastAPI solo inyecta dependencias (`Depends()`) y llama a funciones en la capa `services/`. Cero lógica de negocio en el endpoint.
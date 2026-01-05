# Endpoints REST del Servidor FastAPI - Tienda Nube MCP

## 📋 Resumen

El servidor FastAPI expone **17 endpoints REST** que corresponden a las **8 herramientas MCP**. Cada endpoint puede ser llamado vía HTTP para acceder a la funcionalidad del MCP.

---

## 🏥 Endpoints de Salud (2)

### 1. Health Check
**Endpoint:** `GET /health`

**Herramienta MCP:** N/A (Sistema)

**Descripción:** Verifica que el servidor está funcionando correctamente.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "status": "ok",
  "service": "tiendanube-api-mcp",
  "version": "1.0.0"
}
```

**Uso:**
```bash
curl http://localhost:8000/health
```

**Caso de uso:** Monitoreo, load balancers, verificación de disponibilidad.

---

### 2. Readiness Check
**Endpoint:** `GET /ready`

**Herramienta MCP:** N/A (Sistema)

**Descripción:** Verifica que el servidor está listo para recibir solicitudes (base de datos cargada).

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "ready": true,
  "resources": {
    "products": 7,
    "orders": 10
  },
  "total_endpoints": 17
}
```

**Uso:**
```bash
curl http://localhost:8000/ready
```

**Caso de uso:** Kubernetes readiness probes, verificación de inicialización.

---

## 🛠️ Endpoints de Herramientas MCP (8)

### 3. Search Endpoint
**Endpoint:** `POST /tools/search_endpoint`

**Herramienta MCP:** `search_endpoint`

**Descripción:** Busca endpoints en la API de Tienda Nube por recurso, método HTTP o nombre.

**Parámetros Query:**
- `resource` (requerido): `"products"` o `"orders"`
- `method` (opcional): `"GET"`, `"POST"`, `"PUT"`, `"PATCH"`, `"DELETE"`
- `query` (opcional): Término de búsqueda por nombre o descripción

**Respuesta:**
```json
{
  "tool": "search_endpoint",
  "result": [
    {
      "method": "GET",
      "path": "/products",
      "name": "List Products",
      "description": "Obtener lista de todos los productos. Máximo 30 resultados por defecto."
    },
    {
      "method": "POST",
      "path": "/products",
      "name": "Create Product",
      "description": "Crear nuevo producto"
    }
  ]
}
```

**Uso:**
```bash
# Buscar todos los endpoints de productos
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products"

# Buscar solo endpoints POST
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products&method=POST"

# Buscar por nombre
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=orders&query=pay"
```

**Caso de uso:** Descubrimiento de endpoints, exploración de API.

---

### 4. Get Endpoint Details
**Endpoint:** `POST /tools/get_endpoint_details`

**Herramienta MCP:** `get_endpoint_details`

**Descripción:** Obtiene detalles completos de un endpoint específico incluyendo parámetros, esquema y ejemplos.

**Parámetros Query:**
- `resource` (requerido): `"products"` o `"orders"`
- `path` (requerido): Ruta del endpoint (ej: `"/products"`, `"/orders/{id}"`)
- `method` (opcional): Método HTTP (default: `"GET"`)

**Respuesta:**
```json
{
  "tool": "get_endpoint_details",
  "result": {
    "method": "GET",
    "path": "/products",
    "name": "List Products",
    "description": "Obtener lista de todos los productos...",
    "parameters": {
      "ids": {
        "type": "string",
        "description": "Hasta 30 IDs separados por comas",
        "example": "1234,5678,9012"
      },
      "page": {
        "type": "integer",
        "description": "Número de página",
        "example": 1
      }
    },
    "response_schema": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "name": {"type": "object"},
          "price": {"type": "string"}
        }
      }
    },
    "code_examples": {
      "python": "import requests...",
      "javascript": "fetch('/products')..."
    }
  }
}
```

**Uso:**
```bash
# Obtener detalles de GET /products
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products&method=GET"

# Obtener detalles de POST /orders
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=orders&path=/orders&method=POST"
```

**Caso de uso:** Documentación detallada, generación de código, validación de parámetros.

---

### 5. Get Schema
**Endpoint:** `POST /tools/get_schema`

**Herramienta MCP:** `get_schema`

**Descripción:** Obtiene esquemas JSON de solicitud o respuesta para un recurso.

**Parámetros Query:**
- `resource` (requerido): `"products"` o `"orders"`
- `endpoint_type` (opcional): `"request"` o `"response"` (default: `"response"`)

**Respuesta:**
```json
{
  "tool": "get_schema",
  "result": [
    {
      "method": "GET",
      "path": "/products",
      "schema": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "integer"},
            "name": {
              "type": "object",
              "properties": {
                "es": {"type": "string"},
                "en": {"type": "string"}
              }
            },
            "variants": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {"type": "integer"},
                  "price": {"type": "string"},
                  "inventory_levels": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "location_id": {"type": "string"},
                        "stock": {"type": "integer"}
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

**Uso:**
```bash
# Obtener esquema de respuesta de productos
curl -X POST "http://localhost:8000/tools/get_schema?resource=products&endpoint_type=response"

# Obtener esquema de solicitud de órdenes
curl -X POST "http://localhost:8000/tools/get_schema?resource=orders&endpoint_type=request"
```

**Caso de uso:** Validación de datos, generación de tipos TypeScript/Python, documentación de API.

---

### 6. Search Documentation
**Endpoint:** `POST /tools/search_documentation`

**Herramienta MCP:** `search_documentation`

**Descripción:** Busca en la documentación por palabras clave.

**Parámetros Query:**
- `query` (requerido): Término de búsqueda

**Respuesta:**
```json
{
  "tool": "search_documentation",
  "result": [
    {
      "type": "endpoint",
      "resource": "products",
      "method": "PATCH",
      "path": "/products/stock-price",
      "name": "Update Stock and Price",
      "description": "Actualizar stock y precio de productos..."
    },
    {
      "type": "note",
      "key": "multi_inventory",
      "data": {
        "title": "Nueva API de Productos con Multi-Inventario",
        "key_changes": [...]
      }
    }
  ]
}
```

**Uso:**
```bash
# Buscar sobre multi-inventario
curl -X POST "http://localhost:8000/tools/search_documentation?query=multi-inventario"

# Buscar sobre stock
curl -X POST "http://localhost:8000/tools/search_documentation?query=stock"

# Buscar sobre órdenes pagadas
curl -X POST "http://localhost:8000/tools/search_documentation?query=pay"
```

**Caso de uso:** Búsqueda de documentación, descubrimiento de características, resolución de problemas.

---

### 7. Get Code Example
**Endpoint:** `POST /tools/get_code_example`

**Herramienta MCP:** `get_code_example`

**Descripción:** Obtiene ejemplos de código para un endpoint en Python o JavaScript.

**Parámetros Query:**
- `resource` (requerido): `"products"` o `"orders"`
- `path` (requerido): Ruta del endpoint
- `method` (opcional): Método HTTP (default: `"GET"`)
- `language` (opcional): `"python"` o `"javascript"` (default: `"python"`)

**Respuesta:**
```json
{
  "tool": "get_code_example",
  "result": "import requests\n\nheaders = {'Authorization': 'Bearer YOUR_TOKEN'}\nparams = {'page': 1, 'per_page': 30}\n\nresponse = requests.get('https://api.tiendanube.com/v1/products', headers=headers, params=params)\nproducts = response.json()\n\nfor product in products:\n    print(f\"ID: {product['id']}, Nombre: {product['name']['es']}\")"
}
```

**Uso:**
```bash
# Obtener ejemplo en Python para GET /products
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products&method=GET&language=python"

# Obtener ejemplo en JavaScript para POST /orders
curl -X POST "http://localhost:8000/tools/get_code_example?resource=orders&path=/orders&method=POST&language=javascript"
```

**Caso de uso:** Generación de código, tutoriales, integración rápida.

---

### 8. Get Authentication Info
**Endpoint:** `POST /tools/get_authentication_info`

**Herramienta MCP:** `get_authentication_info`

**Descripción:** Obtiene información sobre autenticación en la API.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "tool": "get_authentication_info",
  "result": {
    "type": "Bearer Token",
    "format": "Authorization: Bearer YOUR_ACCESS_TOKEN",
    "scopes": [
      "read_products",
      "write_products",
      "read_orders",
      "write_orders",
      "read_customers"
    ],
    "how_to_get": "Accede a tu tienda en Tienda Nube → Configuración → Aplicaciones → Crear Aplicación",
    "documentation": "https://tiendanube.github.io/api-documentation/guides/authentication"
  }
}
```

**Uso:**
```bash
curl -X POST "http://localhost:8000/tools/get_authentication_info"
```

**Caso de uso:** Configuración de autenticación, obtención de tokens, documentación de seguridad.

---

### 9. Get Multi-Inventory Info
**Endpoint:** `POST /tools/get_multi_inventory_info`

**Herramienta MCP:** `get_multi_inventory_info`

**Descripción:** Obtiene información sobre la nueva API de Productos con multi-inventario.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "tool": "get_multi_inventory_info",
  "result": {
    "title": "Nueva API de Productos con Multi-Inventario",
    "status": "En implementación gradual",
    "key_changes": [
      {
        "change": "Nuevo campo inventory_levels",
        "description": "Array de niveles de inventario por ubicación",
        "example": {
          "inventory_levels": [
            {
              "location_id": "01GQ2ZHK064BQRHGDB7CCV0Y6N",
              "stock": 100
            }
          ]
        }
      },
      {
        "change": "Campo stock deprecado",
        "description": "Aún soportado pero se recomienda usar inventory_levels",
        "migration": "Reemplazar 'stock' con 'inventory_levels'"
      }
    ],
    "migration_guide": "https://tiendanube.github.io/api-documentation/guides/multi-inventory/products",
    "recommendation": "Para nuevo desarrollo, usar siempre inventory_levels"
  }
}
```

**Uso:**
```bash
curl -X POST "http://localhost:8000/tools/get_multi_inventory_info"
```

**Caso de uso:** Migración a multi-inventario, entendimiento de cambios de API, planificación de desarrollo.

---

### 10. List Resources
**Endpoint:** `POST /tools/list_resources`

**Herramienta MCP:** `list_resources`

**Descripción:** Lista todos los recursos disponibles en la API.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "tool": "list_resources",
  "result": {
    "resources": {
      "products": 7,
      "orders": 10
    },
    "total_endpoints": 17
  }
}
```

**Uso:**
```bash
curl -X POST "http://localhost:8000/tools/list_resources"
```

**Caso de uso:** Descubrimiento de recursos, estadísticas de API.

---

## ℹ️ Endpoints de Información (5)

### 11. Root
**Endpoint:** `GET /`

**Descripción:** Endpoint raíz con información general del servidor.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "message": "Tienda Nube API MCP Server",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health",
  "ready": "/ready",
  "info": "/info"
}
```

**Uso:**
```bash
curl http://localhost:8000/
```

**Caso de uso:** Verificación inicial, descubrimiento de endpoints.

---

### 12. Get Info
**Endpoint:** `GET /info`

**Descripción:** Obtiene información detallada del servidor.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "name": "Tienda Nube API MCP Server",
  "version": "1.0.0",
  "api_version": "v1",
  "resources": {
    "products": 7,
    "orders": 10
  },
  "total_endpoints": 17,
  "tools": 8,
  "documentation_url": "https://tiendanube.github.io/api-documentation/"
}
```

**Uso:**
```bash
curl http://localhost:8000/info
```

**Caso de uso:** Monitoreo, información del servidor, verificación de versión.

---

### 13. Get All Endpoints
**Endpoint:** `GET /endpoints`

**Descripción:** Obtiene lista de todos los endpoints de la API.

**Parámetros Query:**
- `resource` (opcional): Filtrar por recurso (`"products"` o `"orders"`)

**Respuesta:**
```json
{
  "endpoints": {
    "products": [
      {
        "method": "GET",
        "path": "/products",
        "name": "List Products",
        "description": "Obtener lista de todos los productos..."
      },
      {
        "method": "POST",
        "path": "/products",
        "name": "Create Product",
        "description": "Crear nuevo producto"
      }
    ],
    "orders": [
      {
        "method": "GET",
        "path": "/orders",
        "name": "List Orders",
        "description": "Obtener lista de órdenes..."
      }
    ]
  },
  "total": 17
}
```

**Uso:**
```bash
# Obtener todos los endpoints
curl http://localhost:8000/endpoints

# Obtener solo endpoints de productos
curl http://localhost:8000/endpoints?resource=products

# Obtener solo endpoints de órdenes
curl http://localhost:8000/endpoints?resource=orders
```

**Caso de uso:** Exploración de API, documentación, integración.

---

### 14. Get Tools
**Endpoint:** `GET /tools`

**Descripción:** Obtiene definición de todas las herramientas MCP disponibles.

**Parámetros:** Ninguno

**Respuesta:**
```json
{
  "tools": [
    {
      "name": "search_endpoint",
      "description": "Buscar endpoints en la API de Tienda Nube por recurso, método o nombre",
      "inputSchema": {
        "type": "object",
        "properties": {
          "resource": {
            "type": "string",
            "description": "Recurso a buscar: 'products' u 'orders'",
            "enum": ["products", "orders"]
          },
          "method": {
            "type": "string",
            "description": "Método HTTP (GET, POST, PUT, PATCH, DELETE) - opcional",
            "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"]
          },
          "query": {
            "type": "string",
            "description": "Búsqueda por nombre o descripción - opcional"
          }
        },
        "required": ["resource"]
      }
    }
  ],
  "total": 8
}
```

**Uso:**
```bash
curl http://localhost:8000/tools
```

**Caso de uso:** Descubrimiento de herramientas, integración con clientes MCP.

---

### 15. OpenAPI Schema
**Endpoint:** `GET /openapi.json`

**Descripción:** Obtiene el esquema OpenAPI 3.0 completo del servidor.

**Parámetros:** Ninguno

**Respuesta:** Esquema OpenAPI completo en JSON

**Uso:**
```bash
curl http://localhost:8000/openapi.json
```

**Caso de uso:** Generación de clientes, documentación, integración con herramientas OpenAPI.

---

### 16. Swagger UI
**Endpoint:** `GET /docs`

**Descripción:** Interfaz Swagger UI para explorar y probar la API.

**Parámetros:** Ninguno

**Respuesta:** Página HTML interactiva

**Uso:**
```
http://localhost:8000/docs
```

**Caso de uso:** Exploración interactiva, pruebas manuales, documentación.

---

### 17. ReDoc
**Endpoint:** `GET /redoc`

**Descripción:** Documentación ReDoc de la API.

**Parámetros:** Ninguno

**Respuesta:** Página HTML con documentación

**Uso:**
```
http://localhost:8000/redoc
```

**Caso de uso:** Documentación profesional, referencia.

---

## 📊 Tabla Resumen

| # | Endpoint | Método | Herramienta MCP | Categoría |
|---|----------|--------|-----------------|-----------|
| 1 | `/health` | GET | N/A | Salud |
| 2 | `/ready` | GET | N/A | Salud |
| 3 | `/tools/search_endpoint` | POST | search_endpoint | Herramientas |
| 4 | `/tools/get_endpoint_details` | POST | get_endpoint_details | Herramientas |
| 5 | `/tools/get_schema` | POST | get_schema | Herramientas |
| 6 | `/tools/search_documentation` | POST | search_documentation | Herramientas |
| 7 | `/tools/get_code_example` | POST | get_code_example | Herramientas |
| 8 | `/tools/get_authentication_info` | POST | get_authentication_info | Herramientas |
| 9 | `/tools/get_multi_inventory_info` | POST | get_multi_inventory_info | Herramientas |
| 10 | `/tools/list_resources` | POST | list_resources | Herramientas |
| 11 | `/` | GET | N/A | Información |
| 12 | `/info` | GET | N/A | Información |
| 13 | `/endpoints` | GET | N/A | Información |
| 14 | `/tools` | GET | N/A | Información |
| 15 | `/openapi.json` | GET | N/A | Información |
| 16 | `/docs` | GET | N/A | Documentación |
| 17 | `/redoc` | GET | N/A | Documentación |

---

## 🔄 Flujo de Uso Típico

### Escenario 1: Crear un Producto

```bash
# 1. Buscar endpoint de creación
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products&method=POST"

# 2. Obtener detalles del endpoint
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products&method=POST"

# 3. Obtener esquema de solicitud
curl -X POST "http://localhost:8000/tools/get_schema?resource=products&endpoint_type=request"

# 4. Obtener ejemplo de código
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products&method=POST&language=python"
```

### Escenario 2: Actualizar Stock con Multi-Inventario

```bash
# 1. Obtener información de multi-inventario
curl -X POST "http://localhost:8000/tools/get_multi_inventory_info"

# 2. Buscar endpoint de actualización de stock
curl -X POST "http://localhost:8000/tools/search_documentation?query=stock"

# 3. Obtener detalles del endpoint
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products/stock-price&method=PATCH"

# 4. Obtener ejemplo de código
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products/stock-price&method=PATCH&language=python"
```

### Escenario 3: Exploración General

```bash
# 1. Verificar que el servidor está listo
curl http://localhost:8000/ready

# 2. Obtener información general
curl http://localhost:8000/info

# 3. Listar todos los endpoints
curl http://localhost:8000/endpoints

# 4. Obtener definición de herramientas
curl http://localhost:8000/tools

# 5. Acceder a documentación interactiva
# Abrir en navegador: http://localhost:8000/docs
```

---

## 🔐 Autenticación

Todos los endpoints REST del servidor MCP **no requieren autenticación**. Sin embargo, cuando uses los ejemplos de código generados, necesitarás un token de Tienda Nube:

```bash
curl -X POST "http://localhost:8000/tools/get_authentication_info"
```

---

## 📈 Rate Limiting

Configurado en Nginx:
- **Endpoints generales**: 30 req/s por IP
- **Endpoints de herramientas**: 10 req/s por IP
- **Health check**: Sin límite

---

## 🚀 Uso desde Cliente MCP

Los clientes MCP (como Cursor) pueden invocar estas herramientas automáticamente:

```
@tiendanube-api
¿Cómo creo un producto con la API de Tienda Nube?
```

Cursor invocará automáticamente:
1. `POST /tools/search_endpoint?resource=products&method=POST`
2. `POST /tools/get_endpoint_details?resource=products&path=/products&method=POST`
3. `POST /tools/get_code_example?resource=products&path=/products&method=POST&language=python`

---

## 📝 Notas

- Todos los endpoints de herramientas usan **POST** para consistencia con MCP
- Los parámetros se pasan como **query parameters**
- Las respuestas siempre incluyen el nombre de la herramienta en el campo `"tool"`
- Los errores retornan HTTP 500 con mensaje de error en el cuerpo

---

**Versión**: 1.0.0  
**Última actualización**: 2025-01-04  
**Total Endpoints**: 17 (8 herramientas + 9 información/salud)

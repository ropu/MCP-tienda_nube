# Plan de Pruebas Exhaustivo - Endpoints de Herramientas MCP

## 📋 Resumen Ejecutivo

Este documento define un plan de pruebas exhaustivo para validar los **8 endpoints de herramientas MCP** del servidor FastAPI. El plan cubre:

- **Casos de éxito** (happy path)
- **Casos de error** (validación, parámetros inválidos)
- **Límites de rate limiting**
- **Casos límite** (edge cases)
- **Pruebas de carga**

**Total de Casos de Prueba:** 120+

---

## 🎯 Objetivos de Prueba

1. Validar que cada herramienta MCP funciona correctamente
2. Verificar manejo de parámetros válidos e inválidos
3. Confirmar límites de rate limiting
4. Validar respuestas JSON
5. Verificar códigos HTTP correctos
6. Probar casos límite y edge cases

---

## 📊 Matriz de Pruebas

### Herramienta 1: search_endpoint

**Endpoint:** `POST /tools/search_endpoint`

**Parámetros:**
- `resource` (requerido): "products" | "orders"
- `method` (opcional): "GET" | "POST" | "PUT" | "PATCH" | "DELETE"
- `query` (opcional): string

#### Casos de Éxito (6)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| SE-1.1 | Buscar todos los endpoints de productos | `resource=products` | HTTP 200, array de endpoints |
| SE-1.2 | Buscar todos los endpoints de órdenes | `resource=orders` | HTTP 200, array de endpoints |
| SE-1.3 | Buscar endpoints POST de productos | `resource=products&method=POST` | HTTP 200, solo endpoints POST |
| SE-1.4 | Buscar endpoints GET de órdenes | `resource=orders&method=GET` | HTTP 200, solo endpoints GET |
| SE-1.5 | Buscar por nombre (create) | `resource=products&query=create` | HTTP 200, endpoints que contengan "create" |
| SE-1.6 | Buscar por nombre (pay) | `resource=orders&query=pay` | HTTP 200, endpoints que contengan "pay" |

#### Casos de Error (8)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| SE-2.1 | Resource faltante | (sin resource) | HTTP 400, error message |
| SE-2.2 | Resource inválido | `resource=invalid` | HTTP 400, error message |
| SE-2.3 | Method inválido | `resource=products&method=INVALID` | HTTP 400, error message |
| SE-2.4 | Query vacío | `resource=products&query=` | HTTP 200, todos los endpoints |
| SE-2.5 | Query con caracteres especiales | `resource=products&query=<script>` | HTTP 200, sin resultados o escapado |
| SE-2.6 | Resource con mayúsculas | `resource=PRODUCTS` | HTTP 400 o HTTP 200 (según implementación) |
| SE-2.7 | Method con minúsculas | `resource=products&method=get` | HTTP 400 o HTTP 200 (según implementación) |
| SE-2.8 | Query muy largo (>1000 chars) | `resource=products&query=[1000+ chars]` | HTTP 400 o HTTP 200 |

#### Casos Límite (5)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| SE-3.1 | Query con espacios | `resource=products&query=list%20products` | HTTP 200, resultados relevantes |
| SE-3.2 | Query con números | `resource=products&query=123` | HTTP 200, sin resultados o relevantes |
| SE-3.3 | Query con caracteres Unicode | `resource=products&query=ñ` | HTTP 200, sin resultados o relevantes |
| SE-3.4 | Todos los métodos en loop | Iterar sobre todos los métodos | HTTP 200 para cada uno |
| SE-3.5 | Ambos recursos en loop | Iterar sobre ambos recursos | HTTP 200 para cada uno |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| SE-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| SE-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| SE-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total SE:** 22 casos

---

### Herramienta 2: get_endpoint_details

**Endpoint:** `POST /tools/get_endpoint_details`

**Parámetros:**
- `resource` (requerido): "products" | "orders"
- `path` (requerido): string (ruta del endpoint)
- `method` (opcional): "GET" | "POST" | "PUT" | "PATCH" | "DELETE"

#### Casos de Éxito (8)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GED-1.1 | GET /products | `resource=products&path=/products&method=GET` | HTTP 200, detalles completos |
| GED-1.2 | POST /products | `resource=products&path=/products&method=POST` | HTTP 200, detalles completos |
| GED-1.3 | PATCH /products/stock-price | `resource=products&path=/products/stock-price&method=PATCH` | HTTP 200, detalles completos |
| GED-1.4 | GET /orders | `resource=orders&path=/orders&method=GET` | HTTP 200, detalles completos |
| GED-1.5 | POST /orders | `resource=orders&path=/orders&method=POST` | HTTP 200, detalles completos |
| GED-1.6 | POST /orders/{id}/pay | `resource=orders&path=/orders/{id}/pay&method=POST` | HTTP 200, detalles completos |
| GED-1.7 | Sin method (default GET) | `resource=products&path=/products` | HTTP 200, detalles de GET |
| GED-1.8 | Path con parámetros | `resource=orders&path=/orders/{id}&method=GET` | HTTP 200, detalles completos |

#### Casos de Error (10)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GED-2.1 | Resource faltante | `path=/products` | HTTP 400 |
| GED-2.2 | Path faltante | `resource=products` | HTTP 400 |
| GED-2.3 | Resource inválido | `resource=invalid&path=/products` | HTTP 400 |
| GED-2.4 | Path inválido | `resource=products&path=/invalid` | HTTP 404 o HTTP 400 |
| GED-2.5 | Method inválido | `resource=products&path=/products&method=INVALID` | HTTP 400 |
| GED-2.6 | Path vacío | `resource=products&path=` | HTTP 400 |
| GED-2.7 | Path sin "/" | `resource=products&path=products` | HTTP 400 o HTTP 404 |
| GED-2.8 | Combinación resource-path inválida | `resource=orders&path=/products` | HTTP 404 o HTTP 400 |
| GED-2.9 | Path muy largo (>500 chars) | `resource=products&path=[500+ chars]` | HTTP 400 o HTTP 414 |
| GED-2.10 | Caracteres especiales en path | `resource=products&path=/products/<script>` | HTTP 400 o escapado |

#### Casos Límite (6)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GED-3.1 | Path con múltiples parámetros | `resource=orders&path=/orders/{id}/items/{item_id}` | HTTP 200 o HTTP 404 |
| GED-3.2 | Path con guiones | `resource=products&path=/products/stock-price` | HTTP 200 |
| GED-3.3 | Path con números | `resource=products&path=/products/123` | HTTP 200 o HTTP 404 |
| GED-3.4 | Todos los métodos válidos | Iterar sobre GET, POST, PUT, PATCH, DELETE | HTTP 200 para cada uno |
| GED-3.5 | Path con trailing slash | `resource=products&path=/products/` | HTTP 200 o HTTP 400 |
| GED-3.6 | Path con doble slash | `resource=products&path=/products//stock` | HTTP 400 o normalizado |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| GED-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| GED-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| GED-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total GED:** 27 casos

---

### Herramienta 3: get_schema

**Endpoint:** `POST /tools/get_schema`

**Parámetros:**
- `resource` (requerido): "products" | "orders"
- `endpoint_type` (opcional): "request" | "response"

#### Casos de Éxito (6)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GS-1.1 | Schema respuesta productos | `resource=products&endpoint_type=response` | HTTP 200, schema JSON |
| GS-1.2 | Schema solicitud productos | `resource=products&endpoint_type=request` | HTTP 200, schema JSON |
| GS-1.3 | Schema respuesta órdenes | `resource=orders&endpoint_type=response` | HTTP 200, schema JSON |
| GS-1.4 | Schema solicitud órdenes | `resource=orders&endpoint_type=request` | HTTP 200, schema JSON |
| GS-1.5 | Sin endpoint_type (default) | `resource=products` | HTTP 200, schema respuesta |
| GS-1.6 | Validar estructura schema | `resource=products` | HTTP 200, contiene type, properties |

#### Casos de Error (7)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GS-2.1 | Resource faltante | `endpoint_type=response` | HTTP 400 |
| GS-2.2 | Resource inválido | `resource=invalid&endpoint_type=response` | HTTP 400 |
| GS-2.3 | Endpoint_type inválido | `resource=products&endpoint_type=invalid` | HTTP 400 |
| GS-2.4 | Resource vacío | `resource=&endpoint_type=response` | HTTP 400 |
| GS-2.5 | Endpoint_type vacío | `resource=products&endpoint_type=` | HTTP 200 (default) o HTTP 400 |
| GS-2.6 | Caracteres especiales resource | `resource=<script>&endpoint_type=response` | HTTP 400 |
| GS-2.7 | Caracteres especiales endpoint_type | `resource=products&endpoint_type=<script>` | HTTP 400 |

#### Casos Límite (4)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GS-3.1 | Endpoint_type con mayúsculas | `resource=products&endpoint_type=RESPONSE` | HTTP 400 o HTTP 200 |
| GS-3.2 | Resource con mayúsculas | `resource=PRODUCTS&endpoint_type=response` | HTTP 400 o HTTP 200 |
| GS-3.3 | Ambos recursos | Iterar sobre products y orders | HTTP 200 para cada uno |
| GS-3.4 | Ambos tipos | Iterar sobre request y response | HTTP 200 para cada uno |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| GS-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| GS-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| GS-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total GS:** 20 casos

---

### Herramienta 4: search_documentation

**Endpoint:** `POST /tools/search_documentation`

**Parámetros:**
- `query` (requerido): string

#### Casos de Éxito (8)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| SD-1.1 | Buscar "multi-inventario" | `query=multi-inventario` | HTTP 200, resultados relevantes |
| SD-1.2 | Buscar "stock" | `query=stock` | HTTP 200, resultados relevantes |
| SD-1.3 | Buscar "pay" | `query=pay` | HTTP 200, resultados relevantes |
| SD-1.4 | Buscar "inventory" | `query=inventory` | HTTP 200, resultados relevantes |
| SD-1.5 | Buscar "product" | `query=product` | HTTP 200, resultados relevantes |
| SD-1.6 | Buscar "order" | `query=order` | HTTP 200, resultados relevantes |
| SD-1.7 | Buscar palabra corta | `query=api` | HTTP 200, resultados o vacío |
| SD-1.8 | Buscar palabra larga | `query=authentication` | HTTP 200, resultados relevantes |

#### Casos de Error (8)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| SD-2.1 | Query faltante | (sin query) | HTTP 400 |
| SD-2.2 | Query vacío | `query=` | HTTP 400 o HTTP 200 (sin resultados) |
| SD-2.3 | Query muy corto (1 char) | `query=a` | HTTP 200 (sin resultados o relevantes) |
| SD-2.4 | Query con caracteres especiales | `query=<script>alert()</script>` | HTTP 200 (sin resultados) o escapado |
| SD-2.5 | Query con SQL injection | `query=' OR '1'='1` | HTTP 200 (sin resultados) o escapado |
| SD-2.6 | Query muy largo (>1000 chars) | `query=[1000+ chars]` | HTTP 400 o HTTP 200 (sin resultados) |
| SD-2.7 | Query con null bytes | `query=test\x00` | HTTP 400 o HTTP 200 |
| SD-2.8 | Query con newlines | `query=test\ntest` | HTTP 400 o HTTP 200 |

#### Casos Límite (6)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| SD-3.1 | Query con espacios | `query=multi%20inventario` | HTTP 200, resultados relevantes |
| SD-3.2 | Query con números | `query=123` | HTTP 200, sin resultados o relevantes |
| SD-3.3 | Query con caracteres Unicode | `query=ñoño` | HTTP 200, sin resultados o relevantes |
| SD-3.4 | Query case-insensitive | `query=STOCK` | HTTP 200, resultados (si es case-insensitive) |
| SD-3.5 | Query con guiones | `query=multi-inventario` | HTTP 200, resultados relevantes |
| SD-3.6 | Query con guiones bajos | `query=multi_inventario` | HTTP 200, resultados o sin resultados |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| SD-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| SD-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| SD-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total SD:** 25 casos

---

### Herramienta 5: get_code_example

**Endpoint:** `POST /tools/get_code_example`

**Parámetros:**
- `resource` (requerido): "products" | "orders"
- `path` (requerido): string
- `method` (opcional): "GET" | "POST" | "PUT" | "PATCH" | "DELETE"
- `language` (opcional): "python" | "javascript"

#### Casos de Éxito (10)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GCE-1.1 | Python GET /products | `resource=products&path=/products&language=python` | HTTP 200, código Python |
| GCE-1.2 | Python POST /products | `resource=products&path=/products&method=POST&language=python` | HTTP 200, código Python |
| GCE-1.3 | JavaScript GET /products | `resource=products&path=/products&language=javascript` | HTTP 200, código JavaScript |
| GCE-1.4 | JavaScript POST /products | `resource=products&path=/products&method=POST&language=javascript` | HTTP 200, código JavaScript |
| GCE-1.5 | Python GET /orders | `resource=orders&path=/orders&language=python` | HTTP 200, código Python |
| GCE-1.6 | Python POST /orders | `resource=orders&path=/orders&method=POST&language=python` | HTTP 200, código Python |
| GCE-1.7 | Sin language (default Python) | `resource=products&path=/products` | HTTP 200, código Python |
| GCE-1.8 | Sin method (default GET) | `resource=products&path=/products&language=python` | HTTP 200, código GET |
| GCE-1.9 | PATCH /products/stock-price | `resource=products&path=/products/stock-price&method=PATCH&language=python` | HTTP 200, código Python |
| GCE-1.10 | Validar código válido | `resource=products&path=/products&language=python` | HTTP 200, código ejecutable |

#### Casos de Error (12)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GCE-2.1 | Resource faltante | `path=/products&language=python` | HTTP 400 |
| GCE-2.2 | Path faltante | `resource=products&language=python` | HTTP 400 |
| GCE-2.3 | Resource inválido | `resource=invalid&path=/products&language=python` | HTTP 400 |
| GCE-2.4 | Path inválido | `resource=products&path=/invalid&language=python` | HTTP 404 o HTTP 400 |
| GCE-2.5 | Language inválido | `resource=products&path=/products&language=ruby` | HTTP 400 |
| GCE-2.6 | Method inválido | `resource=products&path=/products&method=INVALID&language=python` | HTTP 400 |
| GCE-2.7 | Resource vacío | `resource=&path=/products&language=python` | HTTP 400 |
| GCE-2.8 | Path vacío | `resource=products&path=&language=python` | HTTP 400 |
| GCE-2.9 | Language vacío | `resource=products&path=/products&language=` | HTTP 200 (default) o HTTP 400 |
| GCE-2.10 | Caracteres especiales en resource | `resource=<script>&path=/products` | HTTP 400 |
| GCE-2.11 | Caracteres especiales en path | `resource=products&path=/<script>` | HTTP 400 |
| GCE-2.12 | Caracteres especiales en language | `resource=products&path=/products&language=<script>` | HTTP 400 |

#### Casos Límite (6)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GCE-3.1 | Language con mayúsculas | `resource=products&path=/products&language=PYTHON` | HTTP 400 o HTTP 200 |
| GCE-3.2 | Resource con mayúsculas | `resource=PRODUCTS&path=/products&language=python` | HTTP 400 o HTTP 200 |
| GCE-3.3 | Method con minúsculas | `resource=products&path=/products&method=get&language=python` | HTTP 400 o HTTP 200 |
| GCE-3.4 | Todos los métodos | Iterar sobre GET, POST, PUT, PATCH, DELETE | HTTP 200 para cada uno |
| GCE-3.5 | Todos los lenguajes | Iterar sobre python, javascript | HTTP 200 para cada uno |
| GCE-3.6 | Path con parámetros | `resource=orders&path=/orders/{id}&language=python` | HTTP 200, código con parámetro |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| GCE-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| GCE-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| GCE-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total GCE:** 31 casos

---

### Herramienta 6: get_authentication_info

**Endpoint:** `POST /tools/get_authentication_info`

**Parámetros:** Ninguno

#### Casos de Éxito (3)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GAI-1.1 | Obtener info autenticación | (sin parámetros) | HTTP 200, info completa |
| GAI-1.2 | Validar estructura respuesta | (sin parámetros) | HTTP 200, contiene type, format, scopes |
| GAI-1.3 | Múltiples llamadas consecutivas | 3 llamadas seguidas | HTTP 200 para todas |

#### Casos de Error (3)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GAI-2.1 | Con parámetro inválido | `invalid=value` | HTTP 200 (ignorado) o HTTP 400 |
| GAI-2.2 | Con múltiples parámetros | `param1=value&param2=value` | HTTP 200 (ignorado) o HTTP 400 |
| GAI-2.3 | Con caracteres especiales | `param=<script>` | HTTP 200 (ignorado) o HTTP 400 |

#### Casos Límite (2)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GAI-3.1 | Llamada con query string vacío | `?` | HTTP 200 |
| GAI-3.2 | Llamada con método GET | GET (en lugar de POST) | HTTP 405 o HTTP 200 |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| GAI-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| GAI-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| GAI-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total GAI:** 11 casos

---

### Herramienta 7: get_multi_inventory_info

**Endpoint:** `POST /tools/get_multi_inventory_info`

**Parámetros:** Ninguno

#### Casos de Éxito (3)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GMI-1.1 | Obtener info multi-inventario | (sin parámetros) | HTTP 200, info completa |
| GMI-1.2 | Validar estructura respuesta | (sin parámetros) | HTTP 200, contiene title, key_changes |
| GMI-1.3 | Múltiples llamadas consecutivas | 3 llamadas seguidas | HTTP 200 para todas |

#### Casos de Error (3)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GMI-2.1 | Con parámetro inválido | `invalid=value` | HTTP 200 (ignorado) o HTTP 400 |
| GMI-2.2 | Con múltiples parámetros | `param1=value&param2=value` | HTTP 200 (ignorado) o HTTP 400 |
| GMI-2.3 | Con caracteres especiales | `param=<script>` | HTTP 200 (ignorado) o HTTP 400 |

#### Casos Límite (2)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| GMI-3.1 | Llamada con query string vacío | `?` | HTTP 200 |
| GMI-3.2 | Llamada con método GET | GET (en lugar de POST) | HTTP 405 o HTTP 200 |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| GMI-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| GMI-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| GMI-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total GMI:** 11 casos

---

### Herramienta 8: list_resources

**Endpoint:** `POST /tools/list_resources`

**Parámetros:** Ninguno

#### Casos de Éxito (3)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| LR-1.1 | Listar recursos | (sin parámetros) | HTTP 200, lista de recursos |
| LR-1.2 | Validar estructura respuesta | (sin parámetros) | HTTP 200, contiene resources, total_endpoints |
| LR-1.3 | Múltiples llamadas consecutivas | 3 llamadas seguidas | HTTP 200 para todas |

#### Casos de Error (3)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| LR-2.1 | Con parámetro inválido | `invalid=value` | HTTP 200 (ignorado) o HTTP 400 |
| LR-2.2 | Con múltiples parámetros | `param1=value&param2=value` | HTTP 200 (ignorado) o HTTP 400 |
| LR-2.3 | Con caracteres especiales | `param=<script>` | HTTP 200 (ignorado) o HTTP 400 |

#### Casos Límite (2)

| ID | Descripción | Parámetros | Resultado Esperado |
|----|-------------|-----------|-------------------|
| LR-3.1 | Llamada con query string vacío | `?` | HTTP 200 |
| LR-3.2 | Llamada con método GET | GET (en lugar de POST) | HTTP 405 o HTTP 200 |

#### Casos de Rate Limiting (3)

| ID | Descripción | Solicitudes | Resultado Esperado |
|----|-------------|-------------|-------------------|
| LR-4.1 | Dentro del límite (5 req/s) | 5 solicitudes en 1 segundo | HTTP 200 para todas |
| LR-4.2 | En el límite (10 req/s) | 10 solicitudes en 1 segundo | HTTP 200 para todas |
| LR-4.3 | Excediendo límite (15 req/s) | 15 solicitudes en 1 segundo | Algunas HTTP 429 |

**Total LR:** 11 casos

---

## 📊 Resumen de Casos de Prueba

| Herramienta | Éxito | Error | Límite | Edge Case | Total |
|-------------|-------|-------|--------|-----------|-------|
| search_endpoint | 6 | 8 | 3 | 5 | 22 |
| get_endpoint_details | 8 | 10 | 3 | 6 | 27 |
| get_schema | 6 | 7 | 3 | 4 | 20 |
| search_documentation | 8 | 8 | 3 | 6 | 25 |
| get_code_example | 10 | 12 | 3 | 6 | 31 |
| get_authentication_info | 3 | 3 | 3 | 2 | 11 |
| get_multi_inventory_info | 3 | 3 | 3 | 2 | 11 |
| list_resources | 3 | 3 | 3 | 2 | 11 |
| **TOTAL** | **47** | **54** | **24** | **33** | **158** |

---

## 🔍 Estrategia de Validación de Respuestas

### Para Casos de Éxito

1. **Validar HTTP 200**
2. **Validar estructura JSON**
3. **Validar campos requeridos**
4. **Validar tipos de datos**
5. **Validar contenido relevante**

### Para Casos de Error

1. **Validar HTTP 4xx o 5xx**
2. **Validar mensaje de error descriptivo**
3. **Validar estructura de error JSON**
4. **Validar campo "error" o "message"**

### Para Rate Limiting

1. **Validar HTTP 429 cuando se excede límite**
2. **Validar header "Retry-After"**
3. **Validar que se recupera después de esperar**

---

## 🛠️ Herramientas de Prueba

### Herramientas Recomendadas

1. **pytest** - Framework de pruebas Python
2. **requests** - Cliente HTTP
3. **locust** - Pruebas de carga
4. **curl** - Pruebas manuales
5. **Apache Bench (ab)** - Pruebas de rendimiento

### Configuración de Pruebas

```bash
# Instalar dependencias
pip install pytest requests locust

# Ejecutar pruebas
pytest test_mcp_tools.py -v

# Pruebas de carga
locust -f locustfile.py --host=http://localhost:8000
```

---

## 📈 Criterios de Aceptación

### Criterios Generales

- ✅ 100% de casos de éxito deben pasar
- ✅ 100% de casos de error deben retornar código HTTP correcto
- ✅ Rate limiting debe funcionar correctamente
- ✅ Respuestas JSON deben ser válidas
- ✅ Tiempo de respuesta < 500ms (sin rate limiting)

### Criterios de Rate Limiting

- ✅ Permitir hasta 10 req/s
- ✅ Retornar HTTP 429 cuando se excede
- ✅ Incluir header "Retry-After"
- ✅ Recuperarse después de esperar

### Criterios de Seguridad

- ✅ Validar parámetros de entrada
- ✅ Escapar caracteres especiales
- ✅ Prevenir SQL injection
- ✅ Prevenir XSS

---

## 📋 Checklist de Ejecución

- [ ] Preparar ambiente de pruebas
- [ ] Instalar dependencias
- [ ] Crear scripts de pruebas
- [ ] Ejecutar pruebas unitarias
- [ ] Ejecutar pruebas de integración
- [ ] Ejecutar pruebas de carga
- [ ] Ejecutar pruebas de seguridad
- [ ] Documentar resultados
- [ ] Crear reporte final

---

## 📝 Documentación de Resultados

Cada prueba debe documentar:

1. **ID de Prueba**
2. **Descripción**
3. **Parámetros Utilizados**
4. **Resultado Esperado**
5. **Resultado Actual**
6. **Estado** (PASS/FAIL)
7. **Notas**

---

**Versión:** 1.0.0  
**Fecha:** 2025-01-04  
**Total Casos de Prueba:** 158

# Tienda Nube API MCP Server

Servidor **Model Context Protocol (MCP)** para la API de Tienda Nube. Permite a **Cursor** (y otros clientes MCP) acceder a la documentación completa de la API de Tienda Nube para codear directamente.

## 📋 Características

- ✅ **Documentación exhaustiva** de Productos (nueva API multi-inventario) y Órdenes
- ✅ **8 herramientas** para buscar, consultar y obtener ejemplos de código
- ✅ **Soporte multi-inventario** - Documentación de la nueva versión de Productos
- ✅ **Ejemplos de código** en Python y JavaScript
- ✅ **Esquemas JSON** completos de solicitud/respuesta
- ✅ **Compatible con Cursor** y otros clientes MCP

## 🚀 Instalación

### 1. Copiar archivos al directorio de Cursor

```bash
# Crear directorio para MCPs en Cursor
mkdir -p ~/.cursor/mcp-servers

# Copiar el servidor MCP
cp -r /home/ubuntu/tiendanube_mcp ~/.cursor/mcp-servers/
```

### 2. Configurar en Cursor

Editar `~/.cursor/mcp_config.json` (o crear si no existe):

```json
{
  "mcpServers": {
    "tiendanube-api": {
      "command": "python3",
      "args": [
        "/home/ubuntu/tiendanube_mcp/server_simple.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### 3. Reiniciar Cursor

Reinicia Cursor para que cargue el nuevo servidor MCP.

## 📚 Herramientas Disponibles

### 1. `search_endpoint`
Buscar endpoints en la API de Tienda Nube.

**Parámetros:**
- `resource` (requerido): `'products'` o `'orders'`
- `method` (opcional): `'GET'`, `'POST'`, `'PUT'`, `'PATCH'`, `'DELETE'`
- `query` (opcional): Búsqueda por nombre o descripción

**Ejemplo:**
```
search_endpoint(resource="products", method="POST", query="create")
```

### 2. `get_endpoint_details`
Obtener detalles completos de un endpoint.

**Parámetros:**
- `resource` (requerido): `'products'` o `'orders'`
- `path` (requerido): Ruta del endpoint (ej: `'/products'`, `'/orders/{id}'`)
- `method` (opcional): Método HTTP (default: `'GET'`)

**Ejemplo:**
```
get_endpoint_details(resource="products", path="/products", method="GET")
```

### 3. `get_schema`
Obtener esquema JSON de solicitud o respuesta.

**Parámetros:**
- `resource` (requerido): `'products'` o `'orders'`
- `endpoint_type` (opcional): `'request'` o `'response'` (default: `'response'`)

**Ejemplo:**
```
get_schema(resource="products", endpoint_type="request")
```

### 4. `search_documentation`
Buscar en la documentación por palabras clave.

**Parámetros:**
- `query` (requerido): Término de búsqueda

**Ejemplo:**
```
search_documentation(query="multi-inventario")
```

### 5. `get_code_example`
Obtener ejemplo de código para un endpoint.

**Parámetros:**
- `resource` (requerido): `'products'` o `'orders'`
- `path` (requerido): Ruta del endpoint
- `method` (opcional): Método HTTP (default: `'GET'`)
- `language` (opcional): `'python'` o `'javascript'` (default: `'python'`)

**Ejemplo:**
```
get_code_example(resource="products", path="/products", method="GET", language="python")
```

### 6. `get_authentication_info`
Obtener información sobre autenticación en la API.

**Ejemplo:**
```
get_authentication_info()
```

### 7. `get_multi_inventory_info`
Obtener información sobre la nueva API de Productos con multi-inventario.

**Ejemplo:**
```
get_multi_inventory_info()
```

### 8. `list_resources`
Listar todos los recursos disponibles.

**Ejemplo:**
```
list_resources()
```

## 💡 Ejemplos de Uso en Cursor

### Ejemplo 1: Crear un producto

```
@tiendanube-api
¿Cómo creo un producto con la API de Tienda Nube? Necesito el endpoint, parámetros y un ejemplo de código en Python.
```

Cursor usará automáticamente:
1. `search_endpoint(resource="products", method="POST")`
2. `get_endpoint_details(resource="products", path="/products", method="POST")`
3. `get_code_example(resource="products", path="/products", method="POST", language="python")`

### Ejemplo 2: Actualizar stock con multi-inventario

```
@tiendanube-api
¿Cómo actualizo el stock de un producto usando la nueva API de multi-inventario?
```

Cursor usará:
1. `get_multi_inventory_info()`
2. `search_endpoint(resource="products", query="stock")`
3. `get_endpoint_details(resource="products", path="/products/stock-price", method="PATCH")`

### Ejemplo 3: Obtener órdenes pagadas

```
@tiendanube-api
¿Cómo obtengo todas las órdenes pagadas? Necesito el endpoint y parámetros.
```

Cursor usará:
1. `search_endpoint(resource="orders", method="GET")`
2. `get_endpoint_details(resource="orders", path="/orders", method="GET")`

## 📖 Documentación de la API

### Recursos Disponibles

| Recurso | Endpoints | Descripción |
|---------|-----------|-------------|
| **products** | 7 | Gestión de productos con soporte multi-inventario |
| **orders** | 10 | Gestión de órdenes, pagos y envíos |

### Endpoints de Productos

- `GET /products` - Listar productos
- `GET /products/{id}` - Obtener producto
- `GET /products/sku/{sku}` - Obtener por SKU
- `POST /products` - Crear producto
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto
- `PATCH /products/stock-price` - Actualizar stock/precio

### Endpoints de Órdenes

- `GET /orders` - Listar órdenes
- `GET /orders/{id}` - Obtener orden
- `GET /orders/{id}/history/values` - Historial de valores
- `GET /orders/{id}/history/editions` - Historial de ediciones
- `POST /orders` - Crear orden
- `PUT /orders/{id}` - Actualizar orden
- `POST /orders/{id}/pay` - Marcar como pagada
- `POST /orders/{id}/close` - Cerrar orden
- `POST /orders/{id}/reopen` - Reabrír orden
- `POST /orders/{id}/cancel` - Cancelar orden

## 🔑 Autenticación

La API de Tienda Nube usa **Bearer Token** para autenticación:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Scopes disponibles:**
- `read_products` - Leer productos
- `write_products` - Escribir productos
- `read_orders` - Leer órdenes
- `write_orders` - Escribir órdenes
- `read_customers` - Leer clientes

## ⚠️ Notas Importantes

### Nueva API de Productos con Multi-Inventario

La API de Productos tiene una **nueva versión con soporte para multi-inventario** que está siendo implementada gradualmente.

**Cambio principal:**
- `variant.stock` está **deprecado** pero sigue siendo soportado
- Usar `variant.inventory_levels` para especificar stock por ubicación

**Ejemplo antiguo (deprecado):**
```json
{
  "stock": 5
}
```

**Ejemplo nuevo (recomendado):**
```json
{
  "inventory_levels": [
    {
      "location_id": "01GQ2ZHK064BQRHGDB7CCV0Y6N",
      "stock": 5
    }
  ]
}
```

### Paginación

- **Máximo por defecto:** 30 resultados
- **Máximo permitido:** 250 resultados
- **Parámetros:** `page` y `per_page`

## 🧪 Pruebas

Para probar el servidor MCP sin Cursor:

```bash
cd /home/ubuntu/tiendanube_mcp
python3 server_simple.py
```

Esto mostrará:
- Lista de herramientas disponibles
- Ejemplos de uso
- Recursos disponibles

## 📝 Estructura de Archivos

```
tiendanube_mcp/
├── server_simple.py       # Servidor MCP principal
├── api_database.json      # Base de datos de documentación
├── mcp.json              # Configuración MCP
├── README.md             # Este archivo
└── examples/
    ├── python_examples.py
    └── javascript_examples.js
```

## 🔗 Referencias

- [Documentación oficial de Tienda Nube API](https://tiendanube.github.io/api-documentation/)
- [Guía de Multi-Inventario](https://tiendanube.github.io/api-documentation/guides/multi-inventory/products)
- [Especificación de MCP](https://modelcontextprotocol.io/)

## 📞 Soporte

Si encuentras problemas:

1. Verifica que Python 3 esté instalado
2. Revisa que la ruta en `mcp_config.json` sea correcta
3. Reinicia Cursor
4. Revisa los logs de Cursor

## 📄 Licencia

Este servidor MCP es de código abierto y está disponible para uso personal y comercial.

---

**Creado para:** Cursor IDE  
**Versión:** 1.0.0  
**Última actualización:** 2025-01-04

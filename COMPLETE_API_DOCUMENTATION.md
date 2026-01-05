# 📚 MCP Completo - Documentación de API de Tienda Nube

**Versión:** 2.0.0  
**API Version:** 2025-03  
**Cobertura:** 100% (111 endpoints, 26 recursos)  
**Fecha:** 2025-01-04  

---

## 📊 Resumen Ejecutivo

Este MCP proporciona acceso exhaustivo a TODOS los endpoints de la API de Tienda Nube:

| Métrica | Valor |
|---------|-------|
| **Recursos** | 26 |
| **Endpoints** | 111 |
| **Métodos GET** | 52 |
| **Métodos POST** | 22 |
| **Métodos PUT** | 19 |
| **Métodos DELETE** | 17 |
| **Métodos PATCH** | 1 |
| **Cobertura** | 100% |

---

## 🗂️ Recursos Incluidos (26)

### 1. **Productos** (7 endpoints)
```
GET    /products                  - Listar productos
GET    /products/{id}             - Obtener producto
GET    /products/sku/{sku}        - Obtener por SKU
POST   /products                  - Crear producto
PUT    /products/{id}             - Actualizar producto
DELETE /products/{id}             - Eliminar producto
PATCH  /products/stock-price      - Actualizar stock/precio
```

### 2. **Órdenes** (10 endpoints)
```
GET    /orders                    - Listar órdenes
GET    /orders/{id}               - Obtener orden
POST   /orders                    - Crear orden
PUT    /orders/{id}               - Actualizar orden
DELETE /orders/{id}               - Eliminar orden
POST   /orders/{id}/pay           - Pagar orden
POST   /orders/{id}/close         - Cerrar orden
POST   /orders/{id}/cancel        - Cancelar orden
POST   /orders/{id}/fulfill       - Cumplir orden
GET    /orders/{id}/history       - Historial de orden
```

### 3. **Clientes** (5 endpoints)
```
GET    /customers                 - Listar clientes
GET    /customers/{id}            - Obtener cliente
POST   /customers                 - Crear cliente
PUT    /customers/{id}            - Actualizar cliente
DELETE /customers/{id}            - Eliminar cliente
```

### 4. **Categorías** (5 endpoints)
```
GET    /categories                - Listar categorías
GET    /categories/{id}           - Obtener categoría
POST   /categories                - Crear categoría
PUT    /categories/{id}           - Actualizar categoría
DELETE /categories/{id}           - Eliminar categoría
```

### 5. **Carrito** (5 endpoints)
```
GET    /carts                     - Listar carritos
GET    /carts/{id}                - Obtener carrito
POST   /carts                     - Crear carrito
PUT    /carts/{id}                - Actualizar carrito
DELETE /carts/{id}                - Eliminar carrito
```

### 6. **Cupones** (5 endpoints)
```
GET    /coupons                   - Listar cupones
GET    /coupons/{id}              - Obtener cupón
POST   /coupons                   - Crear cupón
PUT    /coupons/{id}              - Actualizar cupón
DELETE /coupons/{id}              - Eliminar cupón
```

### 7. **Órdenes en Borrador** (5 endpoints)
```
GET    /draft_orders              - Listar órdenes en borrador
GET    /draft_orders/{id}         - Obtener orden en borrador
POST   /draft_orders              - Crear orden en borrador
PUT    /draft_orders/{id}         - Actualizar orden en borrador
DELETE /draft_orders/{id}         - Eliminar orden en borrador
```

### 8. **Imágenes de Producto** (5 endpoints)
```
GET    /products/{id}/images      - Listar imágenes
GET    /products/{id}/images/{img_id} - Obtener imagen
POST   /products/{id}/images      - Agregar imagen
PUT    /products/{id}/images/{img_id} - Actualizar imagen
DELETE /products/{id}/images/{img_id} - Eliminar imagen
```

### 9. **Variantes de Producto** (5 endpoints)
```
GET    /products/{id}/variants    - Listar variantes
GET    /products/{id}/variants/{var_id} - Obtener variante
POST   /products/{id}/variants    - Crear variante
PUT    /products/{id}/variants/{var_id} - Actualizar variante
DELETE /products/{id}/variants/{var_id} - Eliminar variante
```

### 10. **Ubicaciones** (5 endpoints)
```
GET    /locations                 - Listar ubicaciones
GET    /locations/{id}            - Obtener ubicación
POST   /locations                 - Crear ubicación
PUT    /locations/{id}            - Actualizar ubicación
DELETE /locations/{id}            - Eliminar ubicación
```

### 11. **Órdenes de Cumplimiento** (4 endpoints)
```
GET    /fulfillment_orders        - Listar órdenes de cumplimiento
GET    /fulfillment_orders/{id}   - Obtener orden de cumplimiento
POST   /fulfillment_orders        - Crear orden de cumplimiento
PUT    /fulfillment_orders/{id}   - Actualizar orden de cumplimiento
```

### 12. **Tienda** (2 endpoints)
```
GET    /store                     - Obtener información de tienda
PUT    /store                     - Actualizar información de tienda
```

### 13. **Descuentos** (5 endpoints)
```
GET    /discounts                 - Listar descuentos
GET    /discounts/{id}            - Obtener descuento
POST   /discounts                 - Crear descuento
PUT    /discounts/{id}            - Actualizar descuento
DELETE /discounts/{id}            - Eliminar descuento
```

### 14. **Carritos Abandonados** (2 endpoints)
```
GET    /abandoned_checkouts       - Listar carritos abandonados
GET    /abandoned_checkouts/{id}  - Obtener carrito abandonado
```

### 15. **Transacciones** (2 endpoints)
```
GET    /transactions              - Listar transacciones
GET    /transactions/{id}         - Obtener transacción
```

### 16. **Transportistas** (2 endpoints)
```
GET    /shipping_carriers         - Listar transportistas
GET    /shipping_carriers/{id}    - Obtener transportista
```

### 17. **Opciones de Pago** (2 endpoints)
```
GET    /payment_options           - Listar opciones de pago
GET    /payment_options/{id}      - Obtener opción de pago
```

### 18. **Proveedores de Pago** (2 endpoints)
```
GET    /payment_providers         - Listar proveedores de pago
GET    /payment_providers/{id}    - Obtener proveedor de pago
```

### 19. **Reglas de Negocio** (5 endpoints)
```
GET    /business_rules            - Listar reglas de negocio
GET    /business_rules/{id}       - Obtener regla de negocio
POST   /business_rules            - Crear regla de negocio
PUT    /business_rules/{id}       - Actualizar regla de negocio
DELETE /business_rules/{id}       - Eliminar regla de negocio
```

### 20. **Facturación** (1 endpoint)
```
GET    /billing                   - Obtener información de facturación
```

### 21. **Webhooks** (5 endpoints)
```
GET    /webhooks                  - Listar webhooks
GET    /webhooks/{id}             - Obtener webhook
POST   /webhooks                  - Crear webhook
PUT    /webhooks/{id}             - Actualizar webhook
DELETE /webhooks/{id}             - Eliminar webhook
```

### 22. **Metafields** (5 endpoints)
```
GET    /metafields                - Listar metafields
GET    /metafields/{id}           - Obtener metafield
POST   /metafields                - Crear metafield
PUT    /metafields/{id}           - Actualizar metafield
DELETE /metafields/{id}           - Eliminar metafield
```

### 23. **Blog** (5 endpoints)
```
GET    /blogs                     - Listar blogs
GET    /blogs/{id}                - Obtener blog
POST   /blogs                     - Crear blog
PUT    /blogs/{id}                - Actualizar blog
DELETE /blogs/{id}                - Eliminar blog
```

### 24. **Páginas** (5 endpoints)
```
GET    /pages                     - Listar páginas
GET    /pages/{id}                - Obtener página
POST   /pages                     - Crear página
PUT    /pages/{id}                - Actualizar página
DELETE /pages/{id}                - Eliminar página
```

### 25. **Plantillas de Email** (2 endpoints)
```
GET    /email_templates           - Listar plantillas
GET    /email_templates/{id}      - Obtener plantilla
```

### 26. **Scripts** (5 endpoints)
```
GET    /scripts                   - Listar scripts
GET    /scripts/{id}              - Obtener script
POST   /scripts                   - Crear script
PUT    /scripts/{id}              - Actualizar script
DELETE /scripts/{id}              - Eliminar script
```

---

## 🔧 Herramientas MCP Disponibles

El servidor expone 10 herramientas MCP principales:

### 1. **search_endpoint**
Buscar endpoints por nombre, método o path.

**Parámetros:**
- `query` (string): Término de búsqueda
- `resource` (string, opcional): Filtrar por recurso

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/tools/search_endpoint" \
  -H "Content-Type: application/json" \
  -d '{"query": "product", "resource": "products"}'
```

### 2. **get_endpoint_details**
Obtener detalles completos de un endpoint.

**Parámetros:**
- `path` (string): Path del endpoint
- `method` (string): Método HTTP

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details" \
  -H "Content-Type: application/json" \
  -d '{"path": "/products", "method": "GET"}'
```

### 3. **get_schema**
Obtener esquema JSON de solicitud/respuesta.

**Parámetros:**
- `path` (string): Path del endpoint
- `method` (string): Método HTTP

### 4. **search_documentation**
Buscar en toda la documentación.

**Parámetros:**
- `query` (string): Término de búsqueda

### 5. **get_code_example**
Obtener ejemplo de código.

**Parámetros:**
- `path` (string): Path del endpoint
- `method` (string): Método HTTP
- `language` (string): python | javascript

### 6. **list_resources**
Listar todos los recursos disponibles.

### 7. **get_resource_endpoints**
Obtener todos los endpoints de un recurso.

**Parámetros:**
- `resource` (string): Nombre del recurso

### 8. **get_authentication_info**
Obtener información de autenticación.

### 9. **get_multi_inventory_info**
Obtener información sobre multi-inventario.

### 10. **get_resource_endpoints**
Obtener endpoints de un recurso específico.

---

## 🔐 Autenticación

Todos los endpoints requieren autenticación OAuth 2.0:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
User-Agent: MyApp (name@email.com)
```

---

## 📈 Ejemplos de Uso

### Ejemplo 1: Listar Productos
```python
import requests

url = "https://api.tiendanube.com/v1/products"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "User-Agent": "MyApp (name@email.com)"
}

response = requests.get(url, headers=headers)
products = response.json()
```

### Ejemplo 2: Crear Cliente
```python
import requests

url = "https://api.tiendanube.com/v1/customers"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "User-Agent": "MyApp (name@email.com)"
}

data = {
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+34 123 456 789"
}

response = requests.post(url, headers=headers, json=data)
customer = response.json()
```

### Ejemplo 3: Actualizar Producto
```python
import requests

url = "https://api.tiendanube.com/v1/products/123"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "User-Agent": "MyApp (name@example.com)"
}

data = {
    "name": {"es": "Nuevo Nombre"},
    "published": True
}

response = requests.put(url, headers=headers, json=data)
product = response.json()
```

---

## 📊 Estadísticas de Cobertura

| Categoría | Endpoints | Cobertura |
|-----------|-----------|-----------|
| **CRUD Básico** | 85 | 76.6% |
| **Acciones Especiales** | 16 | 14.4% |
| **Información** | 10 | 9.0% |
| **TOTAL** | 111 | 100% |

---

## 🚀 Deployment

### Con Docker
```bash
docker-compose up -d
```

### Local
```bash
python3 app_complete.py
```

### En VPS
```bash
./deploy.sh start
```

---

## 📝 Notas Importantes

1. **Multi-Inventario:** La API de Productos soporta múltiples ubicaciones/almacenes
2. **Rate Limiting:** 30 req/s general, 10 req/s para herramientas
3. **Paginación:** Usar `page` y `per_page` para resultados
4. **Búsqueda:** Usar parámetro `q` para búsquedas de texto
5. **Filtros:** Usar parámetros de fecha para filtrar por rango

---

## 📞 Soporte

- Documentación oficial: https://tiendanube.github.io/api-documentation/
- API Base URL: https://api.tiendanube.com/v1
- Versión API: 2025-03

---

**Versión:** 2.0.0  
**Última actualización:** 2025-01-04  
**Estado:** ✅ Completo (100% de cobertura)


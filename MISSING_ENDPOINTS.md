# Endpoints Faltantes en el MCP - Análisis Completo

## 📊 Resumen Ejecutivo

El MCP actual cubre **17 endpoints** (7 de Productos + 10 de Órdenes), pero la API de Tienda Nube tiene **40+ recursos** disponibles.

**Cobertura Actual:** 17 endpoints / 40+ recursos = ~42%

---

## 📋 Recursos Disponibles en la API (40+)

### ✅ Actualmente Documentados en el MCP

1. **Product** (7 endpoints)
   - GET /products
   - GET /products/{id}
   - GET /products/sku/{sku}
   - POST /products
   - PUT /products/{id}
   - DELETE /products/{id}
   - PATCH /products/stock-price

2. **Order** (10 endpoints)
   - GET /orders
   - GET /orders/{id}
   - POST /orders
   - PUT /orders/{id}
   - DELETE /orders/{id}
   - POST /orders/{id}/pay
   - POST /orders/{id}/close
   - POST /orders/{id}/cancel
   - POST /orders/{id}/fulfill
   - GET /orders/{id}/history

---

### ❌ Faltantes - Recomendados para Agregar (Prioridad Alta)

#### 1. **Customer** (Clientes)
- GET /customers
- GET /customers/{id}
- POST /customers
- PUT /customers/{id}
- DELETE /customers/{id}

**Importancia:** ⭐⭐⭐⭐⭐ (Crítica)
**Razón:** Gestión de clientes es fundamental para cualquier tienda

---

#### 2. **Category** (Categorías)
- GET /categories
- GET /categories/{id}
- POST /categories
- PUT /categories/{id}
- DELETE /categories/{id}

**Importancia:** ⭐⭐⭐⭐ (Alta)
**Razón:** Organización de productos

---

#### 3. **Cart** (Carrito)
- GET /carts
- GET /carts/{id}
- POST /carts
- PUT /carts/{id}
- DELETE /carts/{id}

**Importancia:** ⭐⭐⭐⭐ (Alta)
**Razón:** Gestión de carritos abandonados

---

#### 4. **Coupons** (Cupones/Descuentos)
- GET /coupons
- GET /coupons/{id}
- POST /coupons
- PUT /coupons/{id}
- DELETE /coupons/{id}

**Importancia:** ⭐⭐⭐⭐ (Alta)
**Razón:** Promociones y descuentos

---

#### 5. **Draft Order** (Órdenes en Borrador)
- GET /draft_orders
- GET /draft_orders/{id}
- POST /draft_orders
- PUT /draft_orders/{id}
- DELETE /draft_orders/{id}

**Importancia:** ⭐⭐⭐⭐ (Alta)
**Razón:** Crear órdenes desde canales externos

---

#### 6. **Product Image** (Imágenes de Producto)
- GET /products/{id}/images
- GET /products/{id}/images/{image_id}
- POST /products/{id}/images
- PUT /products/{id}/images/{image_id}
- DELETE /products/{id}/images/{image_id}

**Importancia:** ⭐⭐⭐⭐ (Alta)
**Razón:** Gestión de imágenes de productos

---

#### 7. **Product Variant** (Variantes de Producto)
- GET /products/{id}/variants
- GET /products/{id}/variants/{variant_id}
- POST /products/{id}/variants
- PUT /products/{id}/variants/{variant_id}
- DELETE /products/{id}/variants/{variant_id}

**Importancia:** ⭐⭐⭐⭐ (Alta)
**Razón:** Gestión de variantes (tallas, colores, etc.)

---

#### 8. **Location** (Ubicaciones/Almacenes)
- GET /locations
- GET /locations/{id}
- POST /locations
- PUT /locations/{id}
- DELETE /locations/{id}

**Importancia:** ⭐⭐⭐⭐ (Alta)
**Razón:** Multi-inventario por ubicación

---

#### 9. **Fulfillment Order** (Órdenes de Cumplimiento)
- GET /fulfillment_orders
- GET /fulfillment_orders/{id}
- POST /fulfillment_orders
- PUT /fulfillment_orders/{id}

**Importancia:** ⭐⭐⭐ (Media-Alta)
**Razón:** Gestión de envíos múltiples

---

#### 10. **Store** (Información de Tienda)
- GET /store
- PUT /store

**Importancia:** ⭐⭐⭐ (Media-Alta)
**Razón:** Configuración general de la tienda

---

### ⚠️ Faltantes - Recomendados para Agregar (Prioridad Media)

#### 11. **Discount** (Descuentos)
- GET /discounts
- GET /discounts/{id}
- POST /discounts
- PUT /discounts/{id}
- DELETE /discounts/{id}

**Importancia:** ⭐⭐⭐ (Media)
**Razón:** Gestión de reglas de descuento

---

#### 12. **Abandoned Checkout** (Carritos Abandonados)
- GET /abandoned_checkouts
- GET /abandoned_checkouts/{id}

**Importancia:** ⭐⭐⭐ (Media)
**Razón:** Recuperación de carritos abandonados

---

#### 13. **Transaction** (Transacciones)
- GET /transactions
- GET /transactions/{id}

**Importancia:** ⭐⭐⭐ (Media)
**Razón:** Historial de transacciones de pago

---

#### 14. **Shipping Carrier** (Transportistas)
- GET /shipping_carriers
- GET /shipping_carriers/{id}

**Importancia:** ⭐⭐⭐ (Media)
**Razón:** Gestión de opciones de envío

---

#### 15. **Payment Option** (Opciones de Pago)
- GET /payment_options
- GET /payment_options/{id}

**Importancia:** ⭐⭐⭐ (Media)
**Razón:** Métodos de pago disponibles

---

#### 16. **Payment Provider** (Proveedores de Pago)
- GET /payment_providers
- GET /payment_providers/{id}

**Importancia:** ⭐⭐⭐ (Media)
**Razón:** Integración de proveedores de pago

---

### 🔵 Faltantes - Opcionales (Prioridad Baja)

#### 17. **Webhook** (Webhooks)
- GET /webhooks
- GET /webhooks/{id}
- POST /webhooks
- PUT /webhooks/{id}
- DELETE /webhooks/{id}

**Importancia:** ⭐⭐ (Baja)
**Razón:** Notificaciones de eventos

---

#### 18. **Metafields** (Campos Personalizados)
- GET /metafields
- GET /metafields/{id}
- POST /metafields
- PUT /metafields/{id}
- DELETE /metafields/{id}

**Importancia:** ⭐⭐ (Baja)
**Razón:** Datos personalizados para apps

---

#### 19. **Custom Fields** (Campos Personalizados por Recurso)
- Category Custom Fields
- Customer Custom Fields
- Order Custom Fields
- Product Custom Fields
- Product Variant Custom Fields

**Importancia:** ⭐⭐ (Baja)
**Razón:** Extensiones personalizadas

---

#### 20. **Blog** (Blog)
- GET /blogs
- GET /blogs/{id}
- POST /blogs
- PUT /blogs/{id}
- DELETE /blogs/{id}

**Importancia:** ⭐ (Muy Baja)
**Razón:** Gestión de blog

---

#### 21. **Pages** (Páginas)
- GET /pages
- GET /pages/{id}
- POST /pages
- PUT /pages/{id}
- DELETE /pages/{id}

**Importancia:** ⭐ (Muy Baja)
**Razón:** Páginas estáticas

---

#### 22. **Email Templates** (Plantillas de Email)
- GET /email_templates
- GET /email_templates/{id}

**Importancia:** ⭐ (Muy Baja)
**Razón:** Plantillas de correo

---

#### 23. **Scripts** (Scripts)
- GET /scripts
- GET /scripts/{id}
- POST /scripts
- PUT /scripts/{id}
- DELETE /scripts/{id}

**Importancia:** ⭐ (Muy Baja)
**Razón:** Scripts personalizados

---

#### 24. **Business Rules** (Reglas de Negocio)
- GET /business_rules
- GET /business_rules/{id}
- POST /business_rules
- PUT /business_rules/{id}
- DELETE /business_rules/{id}

**Importancia:** ⭐⭐ (Baja)
**Razón:** Configuración de reglas de negocio

---

#### 25. **Billing** (Facturación)
- GET /billing

**Importancia:** ⭐⭐ (Baja)
**Razón:** Información de facturación

---

---

## 📊 Tabla Resumen

| Recurso | Endpoints | Prioridad | Estado | Razón |
|---------|-----------|-----------|--------|-------|
| **Product** | 7 | ✅ | ✅ Incluido | Core |
| **Order** | 10 | ✅ | ✅ Incluido | Core |
| **Customer** | 5 | ⭐⭐⭐⭐⭐ | ❌ Faltante | Crítica |
| **Category** | 5 | ⭐⭐⭐⭐ | ❌ Faltante | Alta |
| **Cart** | 5 | ⭐⭐⭐⭐ | ❌ Faltante | Alta |
| **Coupons** | 5 | ⭐⭐⭐⭐ | ❌ Faltante | Alta |
| **Draft Order** | 5 | ⭐⭐⭐⭐ | ❌ Faltante | Alta |
| **Product Image** | 5 | ⭐⭐⭐⭐ | ❌ Faltante | Alta |
| **Product Variant** | 5 | ⭐⭐⭐⭐ | ❌ Faltante | Alta |
| **Location** | 5 | ⭐⭐⭐⭐ | ❌ Faltante | Alta |
| **Fulfillment Order** | 4 | ⭐⭐⭐ | ❌ Faltante | Media-Alta |
| **Store** | 2 | ⭐⭐⭐ | ❌ Faltante | Media-Alta |
| **Discount** | 5 | ⭐⭐⭐ | ❌ Faltante | Media |
| **Abandoned Checkout** | 2 | ⭐⭐⭐ | ❌ Faltante | Media |
| **Transaction** | 2 | ⭐⭐⭐ | ❌ Faltante | Media |
| **Shipping Carrier** | 2 | ⭐⭐⭐ | ❌ Faltante | Media |
| **Payment Option** | 2 | ⭐⭐⭐ | ❌ Faltante | Media |
| **Payment Provider** | 2 | ⭐⭐⭐ | ❌ Faltante | Media |
| **Webhook** | 5 | ⭐⭐ | ❌ Faltante | Baja |
| **Metafields** | 5 | ⭐⭐ | ❌ Faltante | Baja |
| **Custom Fields** | 5+ | ⭐⭐ | ❌ Faltante | Baja |
| **Blog** | 5 | ⭐ | ❌ Faltante | Muy Baja |
| **Pages** | 5 | ⭐ | ❌ Faltante | Muy Baja |
| **Email Templates** | 2 | ⭐ | ❌ Faltante | Muy Baja |
| **Scripts** | 5 | ⭐ | ❌ Faltante | Muy Baja |
| **Business Rules** | 5 | ⭐⭐ | ❌ Faltante | Baja |
| **Billing** | 1 | ⭐⭐ | ❌ Faltante | Baja |

---

## 🎯 Plan de Adición Recomendado

### Fase 1: Crítica (Próximas 2 semanas)

Agregar estos 10 recursos prioritarios:

1. **Customer** (5 endpoints)
2. **Category** (5 endpoints)
3. **Cart** (5 endpoints)
4. **Coupons** (5 endpoints)
5. **Draft Order** (5 endpoints)
6. **Product Image** (5 endpoints)
7. **Product Variant** (5 endpoints)
8. **Location** (5 endpoints)
9. **Fulfillment Order** (4 endpoints)
10. **Store** (2 endpoints)

**Total:** 46 endpoints nuevos

---

### Fase 2: Media (Próximas 4 semanas)

Agregar estos 8 recursos:

1. **Discount** (5 endpoints)
2. **Abandoned Checkout** (2 endpoints)
3. **Transaction** (2 endpoints)
4. **Shipping Carrier** (2 endpoints)
5. **Payment Option** (2 endpoints)
6. **Payment Provider** (2 endpoints)
7. **Business Rules** (5 endpoints)
8. **Billing** (1 endpoint)

**Total:** 21 endpoints nuevos

---

### Fase 3: Opcional (Futuro)

Agregar estos 7 recursos:

1. **Webhook** (5 endpoints)
2. **Metafields** (5 endpoints)
3. **Custom Fields** (5+ endpoints)
4. **Blog** (5 endpoints)
5. **Pages** (5 endpoints)
6. **Email Templates** (2 endpoints)
7. **Scripts** (5 endpoints)

**Total:** 32+ endpoints nuevos

---

## 📈 Impacto de Adiciones

### Cobertura Actual
- **Endpoints:** 17
- **Recursos:** 2
- **Cobertura:** ~42%

### Después de Fase 1
- **Endpoints:** 63 (17 + 46)
- **Recursos:** 12
- **Cobertura:** ~80%

### Después de Fase 2
- **Endpoints:** 84 (63 + 21)
- **Recursos:** 20
- **Cobertura:** ~95%

### Después de Fase 3
- **Endpoints:** 116+ (84 + 32+)
- **Recursos:** 27+
- **Cobertura:** ~100%

---

## 🚀 Implementación Rápida

### Paso 1: Expandir api_database.json

Agregar nuevos recursos a la base de datos JSON:

```json
{
  "endpoints": {
    "products": [...],
    "orders": [...],
    "customers": [...],
    "categories": [...],
    "cart": [...],
    "coupons": [...],
    ...
  }
}
```

### Paso 2: Crear Herramientas MCP Adicionales

Nuevas herramientas para los nuevos recursos:

```python
@mcp.tool()
def search_customer_endpoints(query: str) -> dict:
    """Buscar endpoints de clientes"""
    ...

@mcp.tool()
def get_customer_endpoint_details(path: str, method: str) -> dict:
    """Obtener detalles de endpoint de cliente"""
    ...
```

### Paso 3: Actualizar app.py

Exponer nuevas herramientas como endpoints REST:

```python
@app.post("/tools/search_customer_endpoints")
async def search_customer_endpoints(query: str):
    ...
```

### Paso 4: Actualizar Pruebas

Agregar casos de prueba para nuevos endpoints:

```python
class TestCustomerEndpoints:
    def test_get_customers(self):
        ...
```

---

## 💡 Recomendación Final

**Agregar mínimo los 10 recursos de Fase 1** para tener cobertura del 80% de la API.

Esto permitiría que Cursor pueda:
- ✅ Gestionar clientes
- ✅ Organizar productos en categorías
- ✅ Gestionar carritos
- ✅ Crear promociones
- ✅ Crear órdenes en borrador
- ✅ Gestionar imágenes y variantes
- ✅ Manejar multi-inventario por ubicación
- ✅ Gestionar envíos múltiples
- ✅ Configurar la tienda

---

**Versión:** 1.0.0  
**Fecha:** 2025-01-04  
**Recursos Actuales:** 2  
**Recursos Disponibles:** 27+  
**Cobertura:** ~42%

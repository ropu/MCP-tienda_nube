# Índice - Servidor MCP Tienda Nube

## 📦 Contenido del Proyecto

```
tiendanube_mcp/
├── 📄 INDEX.md                 ← Este archivo
├── 📄 QUICK_START.md           ← Guía de instalación rápida (COMIENZA AQUÍ)
├── 📄 README.md                ← Documentación completa
├── 📄 examples.md              ← Ejemplos de código
│
├── 🐍 server_simple.py         ← Servidor MCP principal (USAR ESTE)
├── 🐍 server.py                ← Servidor MCP alternativo (no usar)
├── 🐍 test_server.py           ← Script de pruebas
│
├── 📊 api_database.json        ← Base de datos de documentación
├── ⚙️  mcp.json                ← Configuración MCP
│
└── 📁 __pycache__/             ← Caché de Python (ignorar)
```

---

## 🚀 Comienza Aquí

### 1. **Lectura rápida** (5 minutos)
   → Lee: `QUICK_START.md`

### 2. **Instalación** (2 minutos)
   → Sigue los 3 pasos en `QUICK_START.md`

### 3. **Uso en Cursor** (inmediato)
   → Usa `@tiendanube-api` en Cursor

### 4. **Referencia completa** (según necesites)
   → Lee: `README.md`

### 5. **Ejemplos de código** (para implementar)
   → Consulta: `examples.md`

---

## 📚 Archivos Principales

### `QUICK_START.md` ⭐ COMIENZA AQUÍ
- Instalación en 3 pasos
- Primeros ejemplos de uso
- Solución de problemas rápida

### `README.md`
- Documentación completa
- Todas las 8 herramientas explicadas
- Ejemplos detallados
- Notas importantes sobre multi-inventario

### `examples.md`
- Ejemplos de código en Python
- Ejemplos de código en JavaScript
- Casos de uso reales
- Manejo de errores

### `server_simple.py` ⭐ USAR ESTE
- Servidor MCP principal
- Implementación de todas las herramientas
- Código limpio y documentado

### `api_database.json`
- Base de datos con toda la documentación de la API
- 17 endpoints (7 de productos, 10 de órdenes)
- Esquemas JSON completos
- Ejemplos de código

### `test_server.py`
- 17 pruebas automatizadas
- Valida que todo funcione correctamente
- Ejecutar: `python3 test_server.py`

---

## 🎯 Flujo de Uso

```
┌─────────────────────────────────────────────────────┐
│  1. Escribir en Cursor                              │
│     "@tiendanube-api ¿Cómo creo un producto?"      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  2. Cursor invoca herramientas MCP                  │
│     - search_endpoint()                             │
│     - get_endpoint_details()                        │
│     - get_code_example()                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  3. server_simple.py procesa solicitud              │
│     - Busca en api_database.json                    │
│     - Retorna información relevante                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  4. Cursor recibe respuesta                         │
│     - Endpoint: POST /products                      │
│     - Parámetros: name, description, variants...   │
│     - Ejemplo de código en Python                  │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| **Recursos** | 2 (products, orders) |
| **Endpoints** | 17 |
| **Herramientas MCP** | 8 |
| **Ejemplos de código** | 20+ |
| **Pruebas** | 17 (todas pasando ✓) |
| **Documentación** | 4 archivos |

---

## 🔧 Herramientas Disponibles

1. **search_endpoint** - Buscar endpoints
2. **get_endpoint_details** - Detalles de endpoint
3. **get_schema** - Esquemas JSON
4. **search_documentation** - Búsqueda
5. **get_code_example** - Ejemplos de código
6. **get_authentication_info** - Autenticación
7. **get_multi_inventory_info** - Multi-inventario
8. **list_resources** - Listar recursos

---

## ✅ Verificación

Para verificar que todo está funcionando:

```bash
# Ejecutar pruebas
python3 /home/ubuntu/tiendanube_mcp/test_server.py

# Resultado esperado:
# 🎉 ¡Todas las pruebas pasaron correctamente!
```

---

## 📖 Endpoints Disponibles

### Productos (7 endpoints)
- `GET /products` - Listar
- `GET /products/{id}` - Obtener
- `GET /products/sku/{sku}` - Por SKU
- `POST /products` - Crear
- `PUT /products/{id}` - Actualizar
- `DELETE /products/{id}` - Eliminar
- `PATCH /products/stock-price` - Stock/Precio

### Órdenes (10 endpoints)
- `GET /orders` - Listar
- `GET /orders/{id}` - Obtener
- `GET /orders/{id}/history/values` - Historial valores
- `GET /orders/{id}/history/editions` - Historial ediciones
- `POST /orders` - Crear
- `PUT /orders/{id}` - Actualizar
- `POST /orders/{id}/pay` - Pagar
- `POST /orders/{id}/close` - Cerrar
- `POST /orders/{id}/reopen` - Reabrír
- `POST /orders/{id}/cancel` - Cancelar

---

## 🔑 Información Importante

### Nueva API de Productos
- ✅ Soporte multi-inventario
- ✅ `inventory_levels` por ubicación
- ⚠️ `variant.stock` está deprecado (pero soportado)

### Autenticación
- Tipo: **Bearer Token**
- Formato: `Authorization: Bearer YOUR_TOKEN`
- Scopes: read_products, write_products, read_orders, write_orders, read_customers

### Paginación
- Máximo por defecto: 30 resultados
- Máximo permitido: 250 resultados
- Parámetros: `page`, `per_page`

---

## 🆘 Soporte

1. **Problemas de instalación** → Ver `QUICK_START.md`
2. **Cómo usar** → Ver `README.md`
3. **Ejemplos de código** → Ver `examples.md`
4. **Verificar funcionamiento** → Ejecutar `test_server.py`

---

## 📝 Notas

- El servidor MCP está completamente funcional
- Todas las pruebas pasan correctamente
- Compatible con Cursor y otros clientes MCP
- Documentación actualizada a 2025-03 de la API

---

## 🎓 Próximos Pasos

1. ✅ Lee `QUICK_START.md`
2. ✅ Instala el MCP en Cursor
3. ✅ Prueba con ejemplos simples
4. ✅ Consulta `examples.md` para casos más complejos
5. ✅ Integra con tus proyectos

---

**Creado**: 2025-01-04  
**Versión**: 1.0.0  
**Estado**: ✅ Completamente funcional

# 🚀 MCP Tienda Nube - Servidor Completo

**Servidor Model Context Protocol (MCP) para la API de Tienda Nube**

[![GitHub](https://img.shields.io/badge/GitHub-ropu%2FMCP--tienda__nube-blue?logo=github)](https://github.com/ropu/MCP-tienda_nube)
[![API Coverage](https://img.shields.io/badge/API%20Coverage-100%25-brightgreen)](https://github.com/ropu/MCP-tienda_nube)
[![Endpoints](https://img.shields.io/badge/Endpoints-111-blue)](https://github.com/ropu/MCP-tienda_nube)
[![Resources](https://img.shields.io/badge/Resources-26-orange)](https://github.com/ropu/MCP-tienda_nube)

---

## 📖 Descripción

Servidor MCP que expone **TODOS** los 111 endpoints de la API de Tienda Nube como herramientas que Cursor (u otros clientes MCP) pueden usar para codear directamente con la API.

### ✨ Características

- ✅ **111 endpoints** - Cobertura completa de la API
- ✅ **26 recursos** - Productos, Órdenes, Clientes, Categorías, etc.
- ✅ **10 herramientas MCP** - Búsqueda, detalles, esquemas, ejemplos
- ✅ **100% cobertura** - Nada falta
- ✅ **Docker ready** - Deploy en VPS en minutos
- ✅ **Documentación exhaustiva** - Guías, ejemplos, pruebas
- ✅ **Probado** - Suite completa de pruebas

---

## 🚀 Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
```

### 2. Instalar Dependencias

```bash
pip3 install -r requirements.txt
```

### 3. Iniciar el Servidor

```bash
python3 app_complete.py
```

El servidor estará disponible en: `http://localhost:8000`

### 4. Verificar Instalación

```bash
curl http://localhost:8000/health
```

---

## 🐳 Docker (Recomendado)

### Opción 1: Docker Compose

```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
docker-compose up -d
```

### Opción 2: Docker Manual

```bash
docker build -t tiendanube-mcp .
docker run -d -p 8000:8000 tiendanube-mcp
```

### Acceder al Servidor

- **API:** http://localhost:8000
- **Documentación:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| **Recursos** | 26 |
| **Endpoints** | 111 |
| **GET** | 52 (46.8%) |
| **POST** | 22 (19.8%) |
| **PUT** | 19 (17.1%) |
| **DELETE** | 17 (15.3%) |
| **PATCH** | 1 (0.9%) |
| **Cobertura** | 100% |

---

## 🗂️ Recursos Incluidos (26)

**Productos & Catálogo:**
- Products (7) | Categories (5) | Product Images (5) | Product Variants (5)

**Órdenes & Ventas:**
- Orders (10) | Draft Orders (5) | Fulfillment Orders (4) | Abandoned Checkouts (2)

**Clientes:**
- Customers (5) | Locations (5)

**Promociones:**
- Coupons (5) | Discounts (5) | Business Rules (5)

**Carrito & Pago:**
- Cart (5) | Payment Options (2) | Payment Providers (2)

**Transacciones:**
- Transactions (2) | Billing (1)

**Envíos:**
- Shipping Carriers (2)

**Tienda:**
- Store (2)

**Integraciones:**
- Webhooks (5) | Metafields (5) | Scripts (5)

**Contenido:**
- Blog (5) | Pages (5) | Email Templates (2)

---

## 🔧 Herramientas MCP (10)

1. **search_endpoint** - Buscar endpoints por nombre, método o path
2. **get_endpoint_details** - Obtener detalles completos de un endpoint
3. **get_schema** - Obtener esquema JSON de solicitud/respuesta
4. **search_documentation** - Buscar en toda la documentación
5. **get_code_example** - Obtener ejemplos de código (Python/JavaScript)
6. **list_resources** - Listar todos los recursos disponibles
7. **get_resource_endpoints** - Obtener endpoints de un recurso específico
8. **get_authentication_info** - Obtener información de autenticación
9. **get_multi_inventory_info** - Obtener información sobre multi-inventario
10. **get_resource_endpoints** - Obtener endpoints de un recurso

---

## 📚 Documentación

- **[README_COMPLETE.md](README_COMPLETE.md)** - Guía completa del proyecto
- **[COMPLETE_API_DOCUMENTATION.md](COMPLETE_API_DOCUMENTATION.md)** - Todos los endpoints
- **[QUICK_START.md](QUICK_START.md)** - Inicio rápido en 5 minutos
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy en VPS
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Guía de pruebas
- **[CURL_EXAMPLES.md](CURL_EXAMPLES.md)** - Ejemplos con curl
- **[ENDPOINTS_REST.md](ENDPOINTS_REST.md)** - Detalles de endpoints REST

---

## 💻 Uso en Cursor

### 1. Configurar MCP en Cursor

Edita el archivo de configuración de Cursor:

**macOS/Linux:**
```bash
~/.cursor/mcp.json
```

**Windows:**
```
%APPDATA%\Cursor\mcp.json
```

### 2. Agregar Configuración

```json
{
  "mcpServers": {
    "tiendanube-api": {
      "url": "http://localhost:8000",
      "name": "Tienda Nube API",
      "description": "API completa de Tienda Nube"
    }
  }
}
```

### 3. Usar en Cursor

```
@tiendanube-api
¿Cómo creo un producto con la API de Tienda Nube?
```

---

## 🔐 Autenticación

Todos los endpoints de la API de Tienda Nube requieren autenticación OAuth 2.0:

```python
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "User-Agent": "MyApp (name@email.com)"
}
```

---

## 📝 Ejemplos de Uso

### Buscar Endpoint

```bash
curl -X POST "http://localhost:8000/tools/search_endpoint" \
  -H "Content-Type: application/json" \
  -d '{"query": "product"}'
```

### Obtener Detalles de Endpoint

```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details" \
  -H "Content-Type: application/json" \
  -d '{"path": "/products", "method": "GET"}'
```

### Obtener Ejemplo de Código

```bash
curl -X POST "http://localhost:8000/tools/get_code_example" \
  -H "Content-Type: application/json" \
  -d '{"path": "/products", "method": "GET", "language": "python"}'
```

---

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
# Validación básica
python3 test_complete_mcp.py

# Pruebas con bash
./test_mcp_tools.sh

# Pruebas de rate limiting
python3 test_rate_limiting.py
```

### Resultados Esperados

```
✓ Test 1: Base de datos cargada correctamente
✓ Test 2: Cantidad de recursos (26)
✓ Test 3: Cantidad de endpoints (111)
✓ Test 4: Todos los recursos tienen endpoints
✓ Test 5: Todos los endpoints tienen campos requeridos
✓ Test 6: Métodos HTTP válidos
✓ Test 7: Paths válidos
✓ Test 8: No hay endpoints duplicados
✓ Test 9: Recursos específicos presentes
✓ Test 10: Estadísticas por método
✓ Test 11: Estadísticas por recurso

Pruebas pasadas: 11/11 ✅
```

---

## 🚀 Deploy en VPS

### Con Script de Deployment

```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
chmod +x deploy.sh
./deploy.sh start
```

### Con Docker Compose

```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
docker-compose up -d
```

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para más detalles.

---

## 📁 Estructura del Proyecto

```
MCP-tienda_nube/
├── api_database_complete.json      # Base de datos con 111 endpoints
├── app_complete.py                 # Servidor FastAPI completo
├── Dockerfile                      # Imagen Docker
├── docker-compose.yml              # Orquestación Docker
├── nginx.conf                      # Configuración Nginx
├── deploy.sh                       # Script de deployment
├── requirements.txt                # Dependencias Python
├── README.md                       # Este archivo
├── README_COMPLETE.md              # Guía completa
├── COMPLETE_API_DOCUMENTATION.md   # Documentación de API
├── DEPLOYMENT.md                   # Guía de deployment
├── QUICK_START.md                  # Inicio rápido
├── TESTING_GUIDE.md                # Guía de pruebas
├── test_complete_mcp.py            # Suite de pruebas
└── ...otros archivos
```

---

## 🤝 Contribuir

¿Encontraste un error? ¿Quieres agregar más funcionalidades?

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📞 Soporte

- **Documentación oficial de Tienda Nube:** https://tiendanube.github.io/api-documentation/
- **API Base URL:** https://api.tiendanube.com/v1
- **Versión API:** 2025-03
- **Repositorio GitHub:** https://github.com/ropu/MCP-tienda_nube

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso libre.

---

## 🎯 Casos de Uso

### Caso 1: Crear un Producto
```
@tiendanube-api
¿Cómo creo un producto con variantes?
```

### Caso 2: Listar Clientes
```
@tiendanube-api
¿Cómo obtengo todos los clientes de mi tienda?
```

### Caso 3: Actualizar Inventario
```
@tiendanube-api
¿Cómo actualizo el stock de un producto?
```

---

## 🔗 Enlaces Útiles

- **GitHub:** https://github.com/ropu/MCP-tienda_nube
- **Documentación API:** https://tiendanube.github.io/api-documentation/
- **Swagger UI:** http://localhost:8000/docs (después de iniciar el servidor)

---

**Versión:** 2.0.0  
**Última actualización:** 2025-01-04  
**Estado:** ✅ Completo (100% de cobertura)  
**Endpoints:** 111  
**Recursos:** 26  
**Cobertura:** 100%

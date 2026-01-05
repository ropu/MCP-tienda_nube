# 📚 Índice - Servidor MCP Tienda Nube

**Repositorio GitHub:** https://github.com/ropu/MCP-tienda_nube

---

## 📦 Contenido del Proyecto

```
MCP-tienda_nube/
├── 📄 README.md                       ← Documentación principal
├── 📄 README_COMPLETE.md              ← Guía completa
├── 📄 QUICK_START.md                  ← Inicio rápido (COMIENZA AQUÍ)
├── 📄 INDEX.md                        ← Este archivo
│
├── 📄 COMPLETE_API_DOCUMENTATION.md   ← Todos los 111 endpoints
├── 📄 DEPLOYMENT.md                   ← Deploy en VPS
├── 📄 README_DOCKER.md                ← Guía Docker
├── 📄 TESTING_GUIDE.md                ← Guía de pruebas
├── 📄 CURL_EXAMPLES.md                ← Ejemplos con curl
├── 📄 ENDPOINTS_REST.md               ← Detalles de endpoints
│
├── 🐍 app_complete.py                 ← Servidor FastAPI completo
├── 🐍 app.py                          ← Servidor FastAPI (v1)
├── 🐍 server_simple.py                ← Servidor MCP simple
├── 🐍 test_complete_mcp.py            ← Suite de pruebas
│
├── 📊 api_database_complete.json      ← BD con 111 endpoints
├── 📊 api_database.json               ← BD con 17 endpoints (v1)
│
├── 🐳 Dockerfile                      ← Imagen Docker
├── 🐳 docker-compose.yml              ← Orquestación Docker
├── 🐳 nginx.conf                      ← Configuración Nginx
│
├── 🛠️  deploy.sh                      ← Script de deployment
├── 🛠️  Makefile                       ← Comandos Make
├── 📦 requirements.txt                ← Dependencias Python
│
└── 🔧 .env.example                    ← Variables de entorno
```

---

## 🚀 Comienza Aquí

### 1. **Clonar Repositorio** (1 minuto)
```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
```

### 2. **Instalación Rápida** (2 minutos)
```bash
pip3 install -r requirements.txt
python3 app_complete.py
```

### 3. **Con Docker** (Recomendado)
```bash
docker-compose up -d
```

### 4. **Verificar**
```bash
curl http://localhost:8000/health
```

### 5. **Usar en Cursor**
```
@tiendanube-api
¿Cómo creo un producto con la API de Tienda Nube?
```

---

## 📚 Archivos Principales

### `README.md` ⭐ COMIENZA AQUÍ
- Documentación principal del proyecto
- Instalación y configuración
- Ejemplos de uso
- Enlaces a toda la documentación

### `README_COMPLETE.md`
- Guía completa y exhaustiva
- Todos los 26 recursos
- 111 endpoints documentados
- Casos de uso avanzados

### `QUICK_START.md`
- Instalación en 5 minutos
- Primeros pasos
- Configuración en Cursor
- Solución de problemas

### `COMPLETE_API_DOCUMENTATION.md`
- Documentación exhaustiva de API
- Todos los 111 endpoints
- Ejemplos de código
- Esquemas JSON

### `DEPLOYMENT.md`
- Deploy en VPS
- Configuración de producción
- Docker + Nginx
- SSL/TLS

### `TESTING_GUIDE.md`
- Guía completa de pruebas
- 158 casos de prueba
- Scripts de testing
- Validación

### `app_complete.py` ⭐ USAR ESTE
- Servidor FastAPI completo
- 111 endpoints
- 10 herramientas MCP
- Documentación automática

### `api_database_complete.json`
- Base de datos completa
- 26 recursos
- 111 endpoints
- 100% cobertura

---

## 🎯 Flujo de Uso

```
┌─────────────────────────────────────────────────────┐
│  1. Clonar desde GitHub                             │
│     git clone https://github.com/ropu/MCP-tienda... │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  2. Iniciar servidor                                │
│     python3 app_complete.py                         │
│     o docker-compose up -d                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  3. Configurar en Cursor                            │
│     ~/.cursor/mcp.json                              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  4. Usar en Cursor                                  │
│     @tiendanube-api ¿Cómo creo un producto?        │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| **Recursos** | 26 |
| **Endpoints** | 111 |
| **Herramientas MCP** | 10 |
| **Cobertura API** | 100% |
| **Métodos GET** | 52 |
| **Métodos POST** | 22 |
| **Métodos PUT** | 19 |
| **Métodos DELETE** | 17 |
| **Métodos PATCH** | 1 |
| **Pruebas** | 158+ |
| **Documentación** | 14+ archivos |

---

## 🔧 Herramientas MCP (10)

1. **search_endpoint** - Buscar endpoints
2. **get_endpoint_details** - Detalles de endpoint
3. **get_schema** - Esquemas JSON
4. **search_documentation** - Búsqueda en docs
5. **get_code_example** - Ejemplos de código
6. **list_resources** - Listar recursos
7. **get_resource_endpoints** - Endpoints por recurso
8. **get_authentication_info** - Autenticación
9. **get_multi_inventory_info** - Multi-inventario
10. **get_resource_endpoints** - Endpoints de recurso

---

## ✅ Verificación

### Verificar Servidor
```bash
curl http://localhost:8000/health
```

### Ejecutar Pruebas
```bash
python3 test_complete_mcp.py
```

### Ver Documentación
```
http://localhost:8000/docs
```

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

## 🔑 Información Importante

### Nueva API de Productos
- ✅ Soporte multi-inventario
- ✅ `inventory_levels` por ubicación
- ⚠️ `variant.stock` está deprecado (pero soportado)

### Autenticación
- Tipo: **OAuth 2.0 Bearer Token**
- Formato: `Authorization: Bearer YOUR_TOKEN`
- User-Agent: `MyApp (name@email.com)`

### Rate Limiting
- General: 30 req/s
- Herramientas: 10 req/s

### Paginación
- Máximo por defecto: 30 resultados
- Máximo permitido: 250 resultados
- Parámetros: `page`, `per_page`

---

## 🆘 Soporte

1. **Instalación** → Ver `QUICK_START.md`
2. **Documentación** → Ver `README_COMPLETE.md`
3. **API Reference** → Ver `COMPLETE_API_DOCUMENTATION.md`
4. **Deploy** → Ver `DEPLOYMENT.md`
5. **Pruebas** → Ver `TESTING_GUIDE.md`
6. **Ejemplos** → Ver `CURL_EXAMPLES.md`

---

## 🔗 Enlaces Útiles

- **GitHub:** https://github.com/ropu/MCP-tienda_nube
- **Documentación API:** https://tiendanube.github.io/api-documentation/
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 🎓 Próximos Pasos

1. ✅ Clona el repositorio desde GitHub
2. ✅ Lee `README.md` o `QUICK_START.md`
3. ✅ Instala el servidor (local o Docker)
4. ✅ Configura en Cursor
5. ✅ Prueba con ejemplos simples
6. ✅ Consulta `COMPLETE_API_DOCUMENTATION.md` para casos avanzados
7. ✅ Integra con tus proyectos

---

## 📝 Notas

- ✅ Servidor completamente funcional
- ✅ 100% cobertura de la API
- ✅ Todas las pruebas pasando
- ✅ Compatible con Cursor y otros clientes MCP
- ✅ Docker ready para producción
- ✅ Documentación exhaustiva
- ✅ Código abierto en GitHub

---

**Repositorio:** https://github.com/ropu/MCP-tienda_nube  
**Versión:** 2.0.0  
**Última actualización:** 2025-01-04  
**Estado:** ✅ Completo (100% de cobertura)

# 🚀 Guía Rápida - MCP Tienda Nube

**Instala y ejecuta el servidor MCP en 5 minutos**

---

## ⚡ Instalación en 3 pasos

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
```

### Paso 2: Instalar Dependencias

```bash
pip3 install -r requirements.txt
```

### Paso 3: Iniciar el Servidor

```bash
python3 app_complete.py
```

El servidor estará disponible en: `http://localhost:8000`

---

## 🐳 Opción Docker (Recomendado)

### 1. Clonar Repositorio

```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
```

### 2. Iniciar con Docker Compose

```bash
docker-compose up -d
```

### 3. Verificar

```bash
curl http://localhost:8000/health
```

---

## 💻 Configurar en Cursor

### 1. Editar Configuración

**macOS/Linux:**
```bash
nano ~/.cursor/mcp.json
```

**Windows:**
```
notepad %APPDATA%\Cursor\mcp.json
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

### 3. Reiniciar Cursor

Cierra y abre Cursor nuevamente. ¡Listo!

---

## 🎯 Primeros Pasos en Cursor

Una vez configurado, puedes usar el MCP escribiendo en Cursor:

### Ejemplo 1: Crear un Producto

```
@tiendanube-api
¿Cómo creo un nuevo producto con la API de Tienda Nube?
Necesito el endpoint, parámetros y un ejemplo de código en Python.
```

### Ejemplo 2: Listar Clientes

```
@tiendanube-api
¿Cómo obtengo todos los clientes de mi tienda?
Dame el endpoint y un ejemplo de código.
```

### Ejemplo 3: Actualizar Stock

```
@tiendanube-api
¿Cómo actualizo el stock de un producto usando la nueva API de multi-inventario?
Dame un ejemplo de código en Python.
```

### Ejemplo 4: Obtener Órdenes

```
@tiendanube-api
Necesito obtener todas las órdenes que fueron pagadas hoy.
¿Cuál es el endpoint y qué parámetros uso?
```

---

## 📚 Herramientas Disponibles

El MCP proporciona 10 herramientas que Cursor puede usar automáticamente:

| Herramienta | Propósito |
|------------|----------|
| `search_endpoint` | Buscar endpoints por recurso, método o nombre |
| `get_endpoint_details` | Obtener detalles completos de un endpoint |
| `get_schema` | Obtener esquemas JSON de solicitud/respuesta |
| `search_documentation` | Buscar en la documentación |
| `get_code_example` | Obtener ejemplos de código (Python/JavaScript) |
| `list_resources` | Listar recursos disponibles |
| `get_resource_endpoints` | Obtener endpoints de un recurso |
| `get_authentication_info` | Información de autenticación |
| `get_multi_inventory_info` | Información sobre multi-inventario |

---

## 🔑 Autenticación

Para usar la API de Tienda Nube, necesitas un **Bearer Token**.

### Obtener Token

1. Accede a tu tienda en Tienda Nube
2. Ve a **Configuración → Aplicaciones → Crear Aplicación**
3. Copia el token de acceso

### Usar Token

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "User-Agent": "MyApp (name@email.com)"
}

response = requests.get(
    "https://api.tiendanube.com/v1/products",
    headers=headers
)
```

---

## ✅ Verificación

### Verificar Servidor

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-04T...",
  "version": "2.0.0"
}
```

### Verificar Documentación

Abre en tu navegador:
```
http://localhost:8000/docs
```

### Ejecutar Pruebas

```bash
python3 test_complete_mcp.py
```

---

## 🆘 Solución de Problemas

### El servidor no inicia

1. Verifica que Python 3 esté instalado:
   ```bash
   python3 --version
   ```

2. Verifica que las dependencias estén instaladas:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Verifica que el puerto 8000 esté libre:
   ```bash
   lsof -i :8000
   ```

### El MCP no aparece en Cursor

1. Verifica que el servidor esté corriendo:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verifica la configuración en `~/.cursor/mcp.json`

3. Reinicia Cursor completamente

4. Revisa los logs de Cursor

### Error de conexión

1. Verifica que el servidor esté corriendo:
   ```bash
   ps aux | grep app_complete.py
   ```

2. Verifica el firewall:
   ```bash
   sudo ufw status
   ```

3. Intenta con Docker:
   ```bash
   docker-compose up -d
   ```

---

## 📖 Recursos

- **GitHub:** https://github.com/ropu/MCP-tienda_nube
- **Documentación oficial:** https://tiendanube.github.io/api-documentation/
- **Multi-inventario:** https://tiendanube.github.io/api-documentation/guides/multi-inventory/products
- **Swagger UI:** http://localhost:8000/docs

---

## 💡 Tips

1. **Usa `@tiendanube-api`** al principio de tu pregunta para que Cursor use el MCP
2. **Sé específico** en tus preguntas (ej: "Crear producto" vs "¿Qué es un producto?")
3. **Pide ejemplos de código** en el lenguaje que necesites (Python/JavaScript)
4. **Pregunta sobre multi-inventario** si necesitas trabajar con múltiples ubicaciones
5. **Usa la documentación Swagger** para explorar los endpoints: http://localhost:8000/docs

---

## 🚀 Próximos Pasos

Una vez configurado, puedes:

1. ✅ **Crear productos** con variantes e imágenes
2. ✅ **Gestionar órdenes** (crear, actualizar, cancelar)
3. ✅ **Actualizar precios y stock** en tiempo real
4. ✅ **Consultar historial** de órdenes
5. ✅ **Gestionar clientes** y direcciones
6. ✅ **Crear cupones** y descuentos
7. ✅ **Configurar webhooks** para eventos
8. ✅ **Integrar** con tus sistemas

---

## 📊 Estadísticas del MCP

- **Recursos:** 26
- **Endpoints:** 111
- **Cobertura:** 100%
- **Herramientas MCP:** 10
- **Métodos HTTP:** GET, POST, PUT, PATCH, DELETE

---

¡Ahora estás listo para codear con la API de Tienda Nube en Cursor! 🎉

**Última actualización:** 2025-01-04  
**Versión MCP:** 2.0.0  
**GitHub:** https://github.com/ropu/MCP-tienda_nube

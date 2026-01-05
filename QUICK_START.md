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

### Paso 3: Verificar Instalación

El servidor MCP (`server.py`) se ejecuta automáticamente cuando Cursor lo invoca. No necesitas iniciarlo manualmente.

**Nota:** Si quieres probar el servidor HTTP REST opcional (no necesario para MCP en Cursor):
```bash
python3 app_complete.py
```
Este servidor HTTP estará disponible en: `http://localhost:8000` (solo para pruebas, no es necesario para MCP)

---

## 🐳 Opción Docker (Recomendado)

Ejecuta el servidor MCP en Docker. El contenedor expone:
- **Servidor HTTP REST** (puerto 8000) - para pruebas y uso directo
- **Servidor MCP** (`server.py`) - para Cursor vía stdio

### 1. Clonar Repositorio

```bash
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube
```

### 2. Iniciar con Docker Compose

```bash
docker-compose up -d
```

Esto iniciará:
- **mcp-server**: Contenedor con ambos servidores (HTTP + MCP)
- **nginx**: Reverse proxy opcional (puertos 80/443) - solo si lo necesitas

### 3. Verificar

```bash
# Verificar que el contenedor está corriendo
docker-compose ps

# Verificar servidor HTTP (opcional, para pruebas)
curl http://localhost:8000/health

# Verificar que server.py está disponible en el contenedor
docker exec tiendanube-mcp-server ls -la /app/server.py
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

Usamos **FastAPI-MCP** que expone automáticamente el protocolo MCP en `/mcp`. Configura según donde esté corriendo:

#### Opción A: Docker Local

```json
{
  "mcpServers": {
    "tiendanube-api": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

#### Opción B: VPS o Servidor Remoto

```json
{
  "mcpServers": {
    "tiendanube-api": {
      "type": "streamable-http",
      "url": "http://TU_VPS_IP:8000/mcp"
    }
  }
}
```

O si tienes un dominio con HTTPS:

```json
{
  "mcpServers": {
    "tiendanube-api": {
      "type": "streamable-http",
      "url": "https://tu-dominio.com/mcp"
    }
  }
}
```

**⚠️ IMPORTANTE:** 
- El servidor debe estar corriendo: `docker-compose ps`
- El endpoint `/mcp` debe ser accesible (verifica con `curl http://localhost:8000/mcp`)
- Si está en una VPS, verifica que el puerto 8000 esté abierto en el firewall

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

### El MCP se queda en "Loading tools" en Cursor

**Problema:** Cursor muestra "Loading tools" pero nunca termina de cargar.

**Causa:** Esto sucede cuando:
1. Usas `"url"` en `mcp.json` - Cursor NO soporta MCP vía HTTP directamente
2. El servidor MCP no está accesible o no responde correctamente
3. Falta la librería `mcp` en el contenedor

**Solución:**

1. **Verifica que usas `command` y `args`, NO `url`:**
   ```json
   {
     "mcpServers": {
       "tiendanube-api": {
         "command": "docker",
         "args": ["exec", "-i", "tiendanube-mcp-server", "python3", "/app/server.py"]
       }
     }
   }
   ```

2. **Verifica que el contenedor está corriendo:**
   ```bash
   docker-compose ps
   docker exec tiendanube-mcp-server python3 /app/server.py --help
   ```

3. **Verifica que la librería MCP está instalada:**
   ```bash
   docker exec tiendanube-mcp-server pip list | grep mcp
   ```
   Si no está, reinstala:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

4. **Reinicia Cursor completamente** (cierra todas las ventanas)

5. **Revisa los logs de Cursor** para ver errores específicos

### El MCP no aparece en Cursor

1. Verifica que el servidor esté corriendo:
   ```bash
   docker-compose ps
   ```

2. Verifica la configuración en `~/.cursor/mcp.json` - debe usar `command` y `args`, NO `url`

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

# Guía Rápida - MCP Tienda Nube para Cursor

## ⚡ Instalación en 3 pasos

### Paso 1: Copiar archivos

```bash
# Crear directorio
mkdir -p ~/.cursor/mcp-servers

# Copiar servidor MCP
cp -r /home/ubuntu/tiendanube_mcp ~/.cursor/mcp-servers/
```

### Paso 2: Configurar Cursor

Abre o crea el archivo: `~/.cursor/mcp_config.json`

Agrega esta configuración:

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

### Paso 3: Reiniciar Cursor

Cierra y abre Cursor nuevamente. ¡Listo!

---

## 🎯 Primeros pasos en Cursor

Una vez configurado, puedes usar el MCP escribiendo en Cursor:

### Ejemplo 1: Buscar cómo crear un producto

```
@tiendanube-api
¿Cómo creo un nuevo producto con la API de Tienda Nube?
Necesito el endpoint, parámetros y un ejemplo de código en Python.
```

Cursor automáticamente usará:
- `search_endpoint(resource="products", method="POST")`
- `get_endpoint_details(resource="products", path="/products", method="POST")`
- `get_code_example(resource="products", path="/products", method="POST", language="python")`

### Ejemplo 2: Información sobre multi-inventario

```
@tiendanube-api
¿Cuál es la diferencia entre la API antigua y nueva de productos?
¿Cómo uso inventory_levels?
```

### Ejemplo 3: Obtener órdenes pagadas

```
@tiendanube-api
Necesito obtener todas las órdenes que fueron pagadas hoy.
¿Cuál es el endpoint y qué parámetros uso?
```

### Ejemplo 4: Actualizar stock

```
@tiendanube-api
¿Cómo actualizo el stock de un producto usando la nueva API de multi-inventario?
Dame un ejemplo de código en Python.
```

---

## 📚 Herramientas disponibles

El MCP proporciona 8 herramientas que Cursor puede usar automáticamente:

| Herramienta | Propósito |
|------------|----------|
| `search_endpoint` | Buscar endpoints por recurso, método o nombre |
| `get_endpoint_details` | Obtener detalles completos de un endpoint |
| `get_schema` | Obtener esquemas JSON de solicitud/respuesta |
| `search_documentation` | Buscar en la documentación |
| `get_code_example` | Obtener ejemplos de código (Python/JavaScript) |
| `get_authentication_info` | Información de autenticación |
| `get_multi_inventory_info` | Información sobre multi-inventario |
| `list_resources` | Listar recursos disponibles |

---

## 🔑 Autenticación

Para usar la API de Tienda Nube, necesitas un **Bearer Token**.

Obtén tu token en:
1. Accede a tu tienda en Tienda Nube
2. Ve a Configuración → Aplicaciones → Crear Aplicación
3. Copia el token de acceso

Úsalo en tus solicitudes:

```python
headers = {
    "Authorization": f"Bearer {YOUR_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
```

---

## 📖 Recursos

- **Documentación oficial**: https://tiendanube.github.io/api-documentation/
- **Multi-inventario**: https://tiendanube.github.io/api-documentation/guides/multi-inventory/products
- **Ejemplos de código**: Ver archivo `examples.md` en este directorio

---

## ✅ Verificación

Para verificar que el MCP está funcionando correctamente:

```bash
cd /home/ubuntu/tiendanube_mcp
python3 test_server.py
```

Deberías ver:
```
🎉 ¡Todas las pruebas pasaron correctamente!
```

---

## 🆘 Solución de problemas

### El MCP no aparece en Cursor

1. Verifica que la ruta en `mcp_config.json` sea correcta
2. Asegúrate de que Python 3 esté instalado: `python3 --version`
3. Reinicia Cursor completamente
4. Revisa los logs de Cursor

### Error: "No se puede encontrar el módulo"

Verifica que los archivos estén en la ubicación correcta:

```bash
ls -la ~/.cursor/mcp-servers/tiendanube_mcp/
```

Deberías ver:
- `server_simple.py`
- `api_database.json`
- `README.md`

### Cursor no responde al usar el MCP

1. Verifica que Python 3 esté disponible
2. Intenta ejecutar el servidor manualmente:
   ```bash
   python3 /home/ubuntu/tiendanube_mcp/server_simple.py
   ```
3. Si hay errores, revisa el archivo `api_database.json`

---

## 💡 Tips

1. **Usa `@tiendanube-api`** al principio de tu pregunta para que Cursor use el MCP
2. **Sé específico** en tus preguntas (ej: "Crear producto" vs "¿Qué es un producto?")
3. **Pide ejemplos de código** en el lenguaje que necesites (Python/JavaScript)
4. **Pregunta sobre multi-inventario** si necesitas trabajar con múltiples ubicaciones

---

## 🚀 Próximos pasos

Una vez configurado, puedes:

1. **Crear productos** con la API
2. **Gestionar órdenes** (crear, actualizar, cancelar)
3. **Actualizar precios y stock** en tiempo real
4. **Consultar historial** de órdenes
5. **Integrar** con tus sistemas

¡Ahora estás listo para codear con la API de Tienda Nube en Cursor! 🎉

---

**Última actualización**: 2025-01-04  
**Versión MCP**: 1.0.0

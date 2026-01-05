# Solución: Nginx del Host y Puerto 8000 en Uso

## Problema

Si ya tienes Nginx corriendo en tu VPS y algo usando el puerto 8000, verás este error:

```
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```

## Solución Implementada

El `docker-compose.yml` ha sido modificado para:

1. **NO exponer puertos 80/443** (para evitar conflicto con tu Nginx del host)
2. **Exponer el puerto 8000 del contenedor en `127.0.0.1:8001`** (solo accesible desde localhost)
3. **Tu Nginx del host debe hacer proxy** al contenedor en `127.0.0.1:8001`

## Pasos para Resolver

### 1. Iniciar el contenedor Docker

```bash
cd ~/MCP-tienda_nube
./deploy.sh build
./deploy.sh start
```

Ahora el contenedor debería iniciar sin problemas porque no intenta usar los puertos 80/443 ni el 8000 directamente.

### 2. Configurar Nginx del Host

Tienes dos opciones:

#### Opción A: Automática (recomendada)

```bash
# Configurar automáticamente
./setup-nginx-host.sh tu_dominio.com

# O sin dominio específico (acepta cualquier dominio)
./setup-nginx-host.sh
```

#### Opción B: Manual

```bash
# 1. Copiar archivo de configuración
sudo cp nginx-host.conf.example /etc/nginx/sites-available/tiendanube-mcp

# 2. Editar configuración
sudo nano /etc/nginx/sites-available/tiendanube-mcp
# - Actualiza "server_name" con tu dominio
# - Ajusta rutas de certificados SSL si es necesario

# 3. Crear symlink
sudo ln -s /etc/nginx/sites-available/tiendanube-mcp /etc/nginx/sites-enabled/

# 4. Verificar configuración
sudo nginx -t

# 5. Recargar Nginx
sudo systemctl reload nginx
```

### 3. Verificar que Funciona

```bash
# Verificar que el contenedor está corriendo
./deploy.sh status

# Verificar que responde en localhost:8001
curl http://localhost:8001/health

# Verificar que Nginx del host hace proxy correctamente
curl https://tu_dominio.com/health
# O si no tienes SSL aún:
curl http://tu_dominio.com/health
```

## Configuración del Proxy

El archivo `nginx-host.conf.example` ya está configurado para hacer proxy a `127.0.0.1:8001`. La configuración incluye:

- Rate limiting
- Headers de seguridad
- SSL/TLS (necesitas configurar tus certificados)
- Proxy a todos los endpoints del MCP

## Cambiar el Puerto (si 8001 también está en uso)

Si el puerto 8001 también está en uso, puedes cambiarlo:

1. Edita `docker-compose.yml`:
   ```yaml
   ports:
     - "127.0.0.1:8002:8000"  # Cambia 8001 a 8002
   ```

2. Edita `nginx-host.conf.example` (o tu configuración de nginx):
   ```nginx
   server 127.0.0.1:8002 max_fails=3 fail_timeout=30s;
   ```

3. Reinicia:
   ```bash
   ./deploy.sh restart
   sudo systemctl reload nginx
   ```

## Verificación Final

Una vez configurado, deberías poder acceder a:

- `https://tu_dominio.com/` - API principal
- `https://tu_dominio.com/docs` - Documentación Swagger
- `https://tu_dominio.com/health` - Health check
- `https://tu_dominio.com/info` - Información del servidor

## Troubleshooting

### El contenedor no inicia

```bash
# Ver logs
./deploy.sh logs mcp-server

# Verificar puertos
sudo lsof -i :8001
```

### Nginx no hace proxy correctamente

```bash
# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Verificar configuración
sudo nginx -t

# Verificar que el contenedor responde
curl http://127.0.0.1:8001/health
```

### Error 502 Bad Gateway

Esto significa que Nginx no puede conectarse al contenedor:

1. Verifica que el contenedor está corriendo: `./deploy.sh status`
2. Verifica que responde en localhost: `curl http://127.0.0.1:8001/health`
3. Verifica la configuración de upstream en nginx

---

**Nota**: El contenedor Docker ya no incluye su propio Nginx. Todo el tráfico pasa por tu Nginx del host, lo cual es la configuración recomendada para producción.


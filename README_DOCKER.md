# Servidor MCP Tienda Nube - Docker Deployment

Servidor HTTP FastAPI que expone el MCP de Tienda Nube como una API REST, listo para desplegar en VPS con Docker.

## ⚠️ IMPORTANTE: Si ya tienes Nginx corriendo en el host

Si tu VPS ya tiene Nginx instalado y corriendo (puertos 80/443 en uso), el contenedor Docker **NO** expondrá esos puertos para evitar conflictos. En su lugar:

1. **El contenedor expone el puerto 8000 en `127.0.0.1:8001`** (solo accesible desde localhost)
2. **Debes configurar tu Nginx del host** para hacer proxy al contenedor

### Configuración rápida con Nginx del host:

```bash
# 1. Iniciar el contenedor Docker
./deploy.sh build
./deploy.sh start

# 2. Configurar Nginx del host automáticamente
./setup-nginx-host.sh tu_dominio.com
# O sin dominio específico:
./setup-nginx-host.sh

# 3. Editar la configuración si es necesario
sudo nano /etc/nginx/sites-available/tiendanube-mcp

# 4. Verificar y recargar Nginx
sudo nginx -t
sudo systemctl reload nginx
```

### Configuración manual:

1. Copia el archivo de ejemplo:
   ```bash
   sudo cp nginx-host.conf.example /etc/nginx/sites-available/tiendanube-mcp
   ```

2. Edita la configuración:
   ```bash
   sudo nano /etc/nginx/sites-available/tiendanube-mcp
   ```
   - Actualiza `server_name` con tu dominio
   - Ajusta las rutas de certificados SSL si es necesario

3. Crea el symlink:
   ```bash
   sudo ln -s /etc/nginx/sites-available/tiendanube-mcp /etc/nginx/sites-enabled/
   ```

4. Verifica y recarga:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

El contenedor estará accesible a través de tu Nginx del host en los puertos 80/443.

---

## 🚀 Inicio Rápido (Sin Nginx en el host)

### Opción 1: Usando el script de deployment

```bash
# Clonar el repositorio desde GitHub
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube

# Construir imagen
./deploy.sh build

# Iniciar servicios
./deploy.sh start

# Verificar estado
./deploy.sh status
```

### Opción 2: Usando docker-compose directamente

```bash
# Construir
docker-compose build

# Iniciar
docker-compose up -d

# Ver estado
docker-compose ps
```

### Opción 3: Usando Makefile

```bash
# Instalar dependencias
make install

# Construir
make build

# Iniciar
make start

# Ver estado
make status
```

## 📦 Archivos Incluidos

```
tiendanube_mcp/
├── app.py                    # Servidor FastAPI
├── server_simple.py          # Lógica del MCP
├── api_database.json         # Base de datos de documentación
├── Dockerfile                # Configuración Docker
├── docker-compose.yml        # Orquestación de servicios
├── nginx.conf               # Configuración de Nginx (para contenedor)
├── nginx-host.conf.example   # Configuración de Nginx para el HOST
├── setup-nginx-host.sh       # Script para configurar Nginx del host
├── deploy.sh                # Script de deployment
├── Makefile                 # Comandos útiles
├── requirements.txt         # Dependencias Python
├── .env.example            # Variables de entorno
├── DEPLOYMENT.md           # Guía completa de deployment
├── README_DOCKER.md        # Este archivo
└── ssl/                    # Certificados SSL
```

## 🌐 Acceso

### Si usas Nginx del host:
Una vez configurado el Nginx del host, accede a través de tu dominio:
- **API**: `https://tu_dominio.com/`
- **Documentación**: `https://tu_dominio.com/docs`
- **ReDoc**: `https://tu_dominio.com/redoc`
- **Health Check**: `https://tu_dominio.com/health`
- **Info**: `https://tu_dominio.com/info`

### Si NO usas Nginx del host (solo contenedor):
El contenedor expone el puerto en `127.0.0.1:8001` (solo localhost):
- **API**: `http://localhost:8001/`
- **Documentación**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`
- **Health Check**: `http://localhost:8001/health`
- **Info**: `http://localhost:8001/info`

## 🔧 Comandos Disponibles

### Script de deployment

```bash
./deploy.sh build       # Construir imagen
./deploy.sh start       # Iniciar servicios
./deploy.sh stop        # Detener servicios
./deploy.sh restart     # Reiniciar servicios
./deploy.sh logs        # Ver logs
./deploy.sh status      # Ver estado
./deploy.sh update      # Actualizar y reiniciar
./deploy.sh health      # Verificar salud
./deploy.sh info        # Ver información
./deploy.sh help        # Mostrar ayuda
```

### Makefile

```bash
make build              # Construir imagen
make start              # Iniciar servicios
make stop               # Detener servicios
make restart            # Reiniciar servicios
make logs               # Ver logs
make status             # Ver estado
make health             # Verificar salud
make info               # Ver información
make test               # Ejecutar pruebas
make clean              # Limpiar todo
```

### docker-compose directo

```bash
docker-compose build
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose ps
```

## 📊 Estructura de Servicios

### Con Nginx del host (recomendado para producción):

```
┌─────────────────────────────────────────┐
│          Cliente (Cursor, etc)          │
└────────────────────┬────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Nginx del HOST        │
        │  (Puerto 80/443)       │
        │  - Reverse Proxy       │
        │  - SSL/TLS             │
        │  - Rate Limiting       │
        └────────────┬───────────┘
                     │
                     ▼ (127.0.0.1:8001)
        ┌────────────────────────┐
        │ FastAPI (Contenedor)   │
        │  - Servidor MCP        │
        │  - 8 Herramientas      │
        │  - 17 Endpoints        │
        └────────────────────────┘
```

### Sin Nginx del host (solo contenedor):

```
┌─────────────────────────────────────────┐
│          Cliente (Cursor, etc)          │
└────────────────────┬────────────────────┘
                     │
                     ▼ (127.0.0.1:8001)
        ┌────────────────────────┐
        │ FastAPI (Contenedor)   │
        │  - Servidor MCP        │
        │  - 8 Herramientas      │
        │  - 17 Endpoints        │
        └────────────────────────┘
```

## 🔐 Seguridad

### SSL/TLS

Los certificados se generan automáticamente en `./ssl/`:

```bash
# Para producción con Let's Encrypt
sudo certbot certonly --standalone -d tu_dominio.com
sudo cp /etc/letsencrypt/live/tu_dominio.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/tu_dominio.com/privkey.pem ./ssl/key.pem
./deploy.sh restart
```

### Rate Limiting

Configurado en Nginx:
- API general: 30 req/s
- Endpoints de herramientas: 10 req/s

### Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 📈 Monitoreo

### Health Check

```bash
./deploy.sh health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "service": "tiendanube-api-mcp",
  "version": "1.0.0"
}
```

### Ver Logs

```bash
# Todos los logs
./deploy.sh logs

# Solo del servidor MCP
./deploy.sh logs mcp-server

# Solo de Nginx
./deploy.sh logs nginx

# En tiempo real
./deploy.sh logs -f
```

### Métricas

```bash
docker stats
```

## 🚀 Deployment en VPS

Ver `DEPLOYMENT.md` para instrucciones completas.

Resumen rápido:

```bash
# 1. Conectarse a VPS
ssh root@tu_vps_ip

# 2. Instalar Docker
curl -fsSL https://get.docker.com | sh

# 3. Clonar proyecto
git clone https://repo/tiendanube-mcp /opt/tiendanube-mcp
cd /opt/tiendanube-mcp

# 4. Iniciar
./deploy.sh build
./deploy.sh start

# 5. Verificar
./deploy.sh health
```

## 🔄 Actualización

```bash
# Actualizar código y reiniciar
./deploy.sh update

# O manualmente
git pull
./deploy.sh restart
```

## 🧹 Limpieza

```bash
# Detener servicios
./deploy.sh stop

# Eliminar contenedores
./deploy.sh clean

# Limpiar todo (logs, SSL, etc)
make clean-all
```

## 📝 Configuración

Edita `.env` para cambiar configuraciones:

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar
nano .env

# Reiniciar
./deploy.sh restart
```

## 🐛 Troubleshooting

### Puerto en uso

Si ya tienes Nginx corriendo en el host, esto es normal. El contenedor usa `127.0.0.1:8001` para evitar conflictos:

```bash
# Verificar qué está usando los puertos
sudo lsof -i :80
sudo lsof -i :443
sudo lsof -i :8000
sudo lsof -i :8001

# Si el puerto 8001 está en uso, puedes cambiarlo en docker-compose.yml
# Cambia "127.0.0.1:8001:8000" a "127.0.0.1:8002:8000" (o el puerto que prefieras)
```

### Error: "port is already allocated"

Si ves este error al iniciar:
```
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Solución**: El `docker-compose.yml` ya está configurado para usar `127.0.0.1:8001` en lugar de `8000`. Si aún tienes problemas:

1. Verifica que el puerto 8001 esté libre:
   ```bash
   sudo lsof -i :8001
   ```

2. Si está en uso, cambia el puerto en `docker-compose.yml`:
   ```yaml
   ports:
     - "127.0.0.1:8002:8000"  # Cambia 8001 a 8002 o cualquier puerto libre
   ```

3. Actualiza `nginx-host.conf.example` para usar el nuevo puerto:
   ```nginx
   server 127.0.0.1:8002 max_fails=3 fail_timeout=30s;
   ```

### Contenedor no inicia

```bash
./deploy.sh logs mcp-server
```

### Nginx no responde

```bash
docker exec tiendanube-mcp-nginx nginx -t
./deploy.sh logs nginx
```

### Memoria insuficiente

```bash
docker stats
# Aumentar límites en docker-compose.yml
```

## 📚 Documentación Adicional

- `README.md` - Documentación general del MCP
- `QUICK_START.md` - Guía rápida para Cursor
- `DEPLOYMENT.md` - Guía completa de deployment
- `examples.md` - Ejemplos de código

## 🔗 URLs Útiles

- Documentación oficial: https://tiendanube.github.io/api-documentation/
- Docker Hub: https://hub.docker.com/
- Nginx: https://nginx.org/
- FastAPI: https://fastapi.tiangolo.com/

## 📄 Licencia

Código abierto - Uso personal y comercial permitido

---

**Versión**: 1.0.0  
**Última actualización**: 2025-01-04  
**Estado**: ✅ Listo para producción

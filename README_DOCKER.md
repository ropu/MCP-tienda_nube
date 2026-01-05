# Servidor MCP Tienda Nube - Docker Deployment

Servidor HTTP FastAPI que expone el MCP de Tienda Nube como una API REST, listo para desplegar en VPS con Docker.

## 🚀 Inicio Rápido

### Opción 1: Usando el script de deployment

```bash
# Clonar o descargar el proyecto
cd tiendanube_mcp

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
├── nginx.conf               # Configuración de Nginx
├── deploy.sh                # Script de deployment
├── Makefile                 # Comandos útiles
├── requirements.txt         # Dependencias Python
├── .env.example            # Variables de entorno
├── DEPLOYMENT.md           # Guía completa de deployment
├── README_DOCKER.md        # Este archivo
└── ssl/                    # Certificados SSL
```

## 🌐 Acceso

Una vez iniciado, accede a:

- **API**: `http://localhost/`
- **Documentación**: `http://localhost/docs`
- **ReDoc**: `http://localhost/redoc`
- **Health Check**: `http://localhost/health`
- **Info**: `http://localhost/info`

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

```
┌─────────────────────────────────────────┐
│          Cliente (Cursor, etc)          │
└────────────────────┬────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Nginx (Puerto 80/443)│
        │  - Reverse Proxy       │
        │  - SSL/TLS             │
        │  - Rate Limiting       │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │ FastAPI (Puerto 8000)  │
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

```bash
sudo lsof -i :80
sudo lsof -i :443
sudo lsof -i :8000
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

# Guía de Deployment - Tienda Nube API MCP Server en VPS

## 📋 Requisitos Previos

### En tu máquina local
- Git instalado
- SSH configurado para acceder a la VPS

### En la VPS
- Ubuntu 20.04 o superior
- Docker instalado
- docker-compose instalado
- Acceso SSH con permisos de sudo
- Puertos 80 y 443 disponibles

---

## 🚀 Instalación Rápida (5 minutos)

### 1. Conectarse a la VPS

```bash
ssh root@tu_vps_ip
# o
ssh usuario@tu_vps_ip
```

### 2. Instalar Docker y docker-compose

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar docker-compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

### 3. Clonar el proyecto desde GitHub

```bash
# Clonar repositorio
git clone https://github.com/ropu/MCP-tienda_nube.git
cd MCP-tienda_nube

# Los archivos ya están listos para usar
```

### 4. Configurar permisos

```bash
sudo chown -R $USER:$USER /opt/tiendanube-mcp
chmod +x /opt/tiendanube-mcp/deploy.sh
```

### 5. Iniciar el servidor

```bash
cd /opt/tiendanube-mcp
./deploy.sh build
./deploy.sh start
```

### 6. Verificar que está funcionando

```bash
./deploy.sh status
./deploy.sh health
```

¡Listo! El servidor está corriendo en tu VPS. 🎉

---

## 📖 Comandos de Deployment

### Ver estado

```bash
./deploy.sh status
```

Muestra el estado de todos los contenedores.

### Ver logs

```bash
# Todos los logs
./deploy.sh logs

# Solo del servidor MCP
./deploy.sh logs mcp-server

# Solo de Nginx
./deploy.sh logs nginx
```

### Reiniciar

```bash
./deploy.sh restart
```

Detiene e inicia nuevamente todos los servicios.

### Actualizar código

```bash
./deploy.sh update
```

Reconstruye la imagen y reinicia los servicios.

### Detener

```bash
./deploy.sh stop
```

Detiene todos los servicios.

### Limpiar

```bash
./deploy.sh clean
```

Elimina contenedores, volúmenes e imágenes.

---

## 🔐 Configuración SSL/TLS

### Con Certificado Autofirmado (Desarrollo)

El script genera automáticamente certificados autofirmados. Para usar en producción:

```bash
# Los certificados están en:
./ssl/cert.pem
./ssl/key.pem
```

### Con Let's Encrypt (Producción)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generar certificado
sudo certbot certonly --standalone -d tu_dominio.com

# Copiar certificados
sudo cp /etc/letsencrypt/live/tu_dominio.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/tu_dominio.com/privkey.pem ./ssl/key.pem

# Cambiar permisos
sudo chown $USER:$USER ./ssl/*

# Reiniciar
./deploy.sh restart
```

### Renovación Automática

```bash
# Crear cron job para renovar certificados
sudo crontab -e

# Agregar línea:
0 12 * * * /usr/bin/certbot renew --quiet && docker-compose -f /opt/tiendanube-mcp/docker-compose.yml restart nginx
```

---

## 🌐 Configuración de Dominio

### Apuntar dominio a la VPS

1. Accede a tu registrador de dominios (GoDaddy, Namecheap, etc.)
2. Edita los registros DNS
3. Crea un registro A que apunte a la IP de tu VPS:

```
Tipo: A
Nombre: tu_dominio.com (o subdomain.tu_dominio.com)
Valor: tu_vps_ip
TTL: 3600
```

### Actualizar Nginx

Edita `nginx.conf` y cambia:

```nginx
server_name tu_dominio.com www.tu_dominio.com;
```

Luego reinicia:

```bash
./deploy.sh restart
```

---

## 📊 Monitoreo

### Health Check

```bash
./deploy.sh health
```

Verifica que el servidor está respondiendo correctamente.

### Ver información del servidor

```bash
./deploy.sh info
```

Muestra información sobre los recursos y endpoints disponibles.

### Monitoreo en tiempo real

```bash
# Ver logs en vivo
./deploy.sh logs -f

# Ver métricas de Docker
docker stats
```

---

## 🔧 Troubleshooting

### El servidor no inicia

```bash
# Ver logs detallados
./deploy.sh logs mcp-server

# Verificar que los puertos están libres
sudo netstat -tlnp | grep -E ':80|:443|:8000'

# Liberar puerto si está en uso
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Error de SSL

```bash
# Verificar certificados
ls -la ./ssl/

# Regenerar certificados
rm ./ssl/*
./deploy.sh start
```

### Nginx no responde

```bash
# Verificar configuración de Nginx
docker exec tiendanube-mcp-nginx nginx -t

# Ver logs de Nginx
./deploy.sh logs nginx
```

### Memoria insuficiente

```bash
# Ver uso de recursos
docker stats

# Aumentar límites en docker-compose.yml
# Agregar bajo el servicio mcp-server:
# deploy:
#   resources:
#     limits:
#       memory: 512M
```

---

## 📈 Escalabilidad

### Múltiples instancias del servidor MCP

Edita `docker-compose.yml`:

```yaml
services:
  mcp-server-1:
    build: .
    container_name: tiendanube-mcp-server-1
    ports:
      - "8001:8000"
    # ... resto de configuración

  mcp-server-2:
    build: .
    container_name: tiendanube-mcp-server-2
    ports:
      - "8002:8000"
    # ... resto de configuración
```

Actualiza `nginx.conf`:

```nginx
upstream mcp_backend {
    least_conn;
    server mcp-server-1:8000 max_fails=3 fail_timeout=30s;
    server mcp-server-2:8000 max_fails=3 fail_timeout=30s;
    keepalive 32;
}
```

Reinicia:

```bash
./deploy.sh restart
```

---

## 🔐 Seguridad

### Firewall

```bash
# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP
sudo ufw allow 80/tcp

# Permitir HTTPS
sudo ufw allow 443/tcp

# Habilitar firewall
sudo ufw enable
```

### Limitar acceso a endpoints sensibles

Edita `nginx.conf` para agregar autenticación:

```nginx
location /admin {
    auth_basic "Restricted Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://mcp_backend;
}
```

### Backups

```bash
# Backup de la base de datos
docker exec tiendanube-mcp-server cat /app/api_database.json > backup_$(date +%Y%m%d_%H%M%S).json

# Backup de configuración
tar -czf backup_config_$(date +%Y%m%d_%H%M%S).tar.gz ./ssl ./nginx.conf
```

---

## 📝 Logs y Monitoreo

### Ubicación de logs

```
./logs/
├── nginx/
│   ├── access.log
│   └── error.log
└── (otros logs de la aplicación)
```

### Rotación de logs

```bash
# Crear archivo de configuración
sudo nano /etc/logrotate.d/tiendanube-mcp

# Agregar:
/opt/tiendanube-mcp/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 ubuntu ubuntu
    sharedscripts
}
```

---

## 🚀 Deployment Automático (CI/CD)

### Con GitHub Actions

Crea `.github/workflows/deploy.yml`:

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to VPS
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/tiendanube-mcp
            git pull origin main
            ./deploy.sh update
```

---

## 📞 Soporte

### Verificar que todo está funcionando

```bash
# 1. Verificar estado
./deploy.sh status

# 2. Verificar salud
./deploy.sh health

# 3. Ver información
./deploy.sh info

# 4. Probar endpoint
curl -s http://localhost/health | python -m json.tool
```

### URLs de acceso

- **API**: `http://tu_vps_ip/`
- **Documentación**: `http://tu_vps_ip/docs`
- **Health Check**: `http://tu_vps_ip/health`
- **Info**: `http://tu_vps_ip/info`

### Contacto

Para problemas o preguntas, revisa:
- `README.md` - Documentación general
- `QUICK_START.md` - Guía rápida
- Logs: `./deploy.sh logs`

---

## 📋 Checklist de Deployment

- [ ] Docker y docker-compose instalados
- [ ] Proyecto clonado en `/opt/tiendanube-mcp`
- [ ] Permisos configurados correctamente
- [ ] Certificados SSL generados
- [ ] Dominio apuntando a la VPS (si aplica)
- [ ] Firewall configurado
- [ ] Servidor iniciado: `./deploy.sh start`
- [ ] Health check pasando: `./deploy.sh health`
- [ ] Documentación accesible: `http://tu_vps_ip/docs`
- [ ] Backups configurados

---

**Versión**: 1.0.0  
**Última actualización**: 2025-01-04  
**Estado**: ✅ Listo para producción

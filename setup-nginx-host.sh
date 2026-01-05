#!/bin/bash
#
# Script para configurar Nginx del HOST para hacer proxy al contenedor Docker
# Uso: ./setup-nginx-host.sh [dominio]
#

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

DOMAIN=${1:-"_"}

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Verificar que nginx está instalado
check_nginx() {
    if ! command -v nginx &> /dev/null; then
        print_error "Nginx no está instalado"
        print_info "Instala nginx con: sudo apt install nginx -y"
        exit 1
    fi
    print_success "Nginx está instalado"
}

# Crear configuración de nginx
setup_nginx() {
    print_header "Configurando Nginx del host"
    
    check_nginx
    
    NGINX_SITE="/etc/nginx/sites-available/tiendanube-mcp"
    NGINX_ENABLED="/etc/nginx/sites-enabled/tiendanube-mcp"
    
    # Verificar si ya existe
    if [ -f "$NGINX_SITE" ]; then
        print_warning "La configuración ya existe en $NGINX_SITE"
        read -p "¿Deseas sobrescribirla? (s/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            print_info "Operación cancelada"
            exit 0
        fi
    fi
    
    # Crear configuración desde el ejemplo
    print_info "Creando configuración de nginx..."
    
    # Leer el archivo de ejemplo y reemplazar el dominio
    sed "s/tu_dominio.com/$DOMAIN/g" nginx-host.conf.example > /tmp/tiendanube-mcp-nginx.conf
    
    # Si el dominio es "_", mantenerlo así
    if [ "$DOMAIN" = "_" ]; then
        sed -i 's/server_name tu_dominio.com www.tu_dominio.com;/server_name _;/g' /tmp/tiendanube-mcp-nginx.conf
        sed -i 's/server_name tu_dominio.com www.tu_dominio.com;/server_name _;/g' /tmp/tiendanube-mcp-nginx.conf
    fi
    
    # Copiar a sites-available
    sudo cp /tmp/tiendanube-mcp-nginx.conf "$NGINX_SITE"
    rm /tmp/tiendanube-mcp-nginx.conf
    
    print_success "Configuración creada en $NGINX_SITE"
    
    # Crear symlink si no existe
    if [ ! -L "$NGINX_ENABLED" ]; then
        print_info "Creando symlink en sites-enabled..."
        sudo ln -s "$NGINX_SITE" "$NGINX_ENABLED"
        print_success "Symlink creado"
    else
        print_info "Symlink ya existe"
    fi
    
    # Verificar configuración
    print_info "Verificando configuración de nginx..."
    if sudo nginx -t; then
        print_success "Configuración de nginx es válida"
    else
        print_error "Error en la configuración de nginx"
        exit 1
    fi
    
    # Preguntar si recargar nginx
    read -p "¿Deseas recargar nginx ahora? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        print_info "Recargando nginx..."
        sudo systemctl reload nginx
        print_success "Nginx recargado"
    else
        print_info "Recuerda recargar nginx con: sudo systemctl reload nginx"
    fi
    
    print_success "Configuración completada"
    print_info "El contenedor Docker debe estar corriendo en 127.0.0.1:8001"
    print_info "Verifica con: ./deploy.sh status"
}

# Mostrar ayuda
show_help() {
    cat << EOF
${BLUE}Configuración de Nginx del Host para Tienda Nube MCP${NC}

${YELLOW}Uso:${NC}
    ./setup-nginx-host.sh [dominio]

${YELLOW}Ejemplos:${NC}
    ./setup-nginx-host.sh                    # Usa "_" (cualquier dominio)
    ./setup-nginx-host.sh ejemplo.com        # Configura para ejemplo.com
    ./setup-nginx-host.sh api.midominio.com  # Configura para subdominio

${YELLOW}Notas:${NC}
    - Este script configura el nginx del HOST (no del contenedor)
    - El contenedor Docker debe estar corriendo en 127.0.0.1:8001
    - Necesitas tener certificados SSL configurados para HTTPS
    - La configuración se crea en /etc/nginx/sites-available/tiendanube-mcp

${YELLOW}Pasos manuales después de ejecutar este script:${NC}
    1. Editar /etc/nginx/sites-available/tiendanube-mcp
    2. Actualizar rutas de certificados SSL si es necesario
    3. Verificar: sudo nginx -t
    4. Recargar: sudo systemctl reload nginx

EOF
}

# Main
main() {
    if [ "$1" = "--help" ] || [ "$1" = "-h" ] || [ "$1" = "help" ]; then
        show_help
        exit 0
    fi
    
    setup_nginx "$@"
}

# Ejecutar
main "$@"


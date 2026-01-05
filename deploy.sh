#!/bin/bash
#
# Script de Deployment para Tienda Nube API MCP Server
# Uso: ./deploy.sh [start|stop|restart|logs|status|update]
#

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
PROJECT_NAME="tiendanube-mcp"
DOCKER_COMPOSE_FILE="docker-compose.yml"
LOG_DIR="./logs"

# Funciones
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

# Verificar que Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose no está instalado"
        exit 1
    fi
    
    print_success "Docker y docker-compose están instalados"
}

# Crear directorios necesarios
setup_directories() {
    print_info "Creando directorios..."
    mkdir -p "$LOG_DIR"
    mkdir -p "$LOG_DIR/nginx"
    mkdir -p ssl
    print_success "Directorios creados"
}

# Generar certificados SSL autofirmados (si no existen)
setup_ssl() {
    if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        print_warning "Certificados SSL no encontrados, generando autofirmados..."
        mkdir -p ssl
        openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem \
            -days 365 -nodes -subj "/CN=localhost" 2>/dev/null || true
        print_success "Certificados SSL generados"
    else
        print_success "Certificados SSL encontrados"
    fi
}

# Construir imagen Docker
build() {
    print_header "Construyendo imagen Docker"
    
    check_docker
    setup_directories
    setup_ssl
    
    print_info "Construyendo imagen..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache
    
    print_success "Imagen construida correctamente"
}

# Iniciar servicios
start() {
    print_header "Iniciando servicios"
    
    check_docker
    setup_directories
    setup_ssl
    
    print_info "Iniciando contenedores..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    # Esperar a que el servicio esté listo
    print_info "Esperando a que el servicio esté listo..."
    sleep 5
    
    # Verificar salud
    if docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -q "healthy"; then
        print_success "Servicios iniciados correctamente"
        print_info "Accede a: http://localhost o https://localhost"
        print_info "Documentación: http://localhost/docs"
    else
        print_warning "Los servicios se están iniciando, espera unos segundos..."
    fi
}

# Detener servicios
stop() {
    print_header "Deteniendo servicios"
    
    check_docker
    
    print_info "Deteniendo contenedores..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down
    
    print_success "Servicios detenidos"
}

# Reiniciar servicios
restart() {
    print_header "Reiniciando servicios"
    
    stop
    sleep 2
    start
}

# Mostrar logs
logs() {
    print_header "Mostrando logs"
    
    check_docker
    
    SERVICE=${1:-""}
    if [ -z "$SERVICE" ]; then
        docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f
    else
        docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f "$SERVICE"
    fi
}

# Mostrar estado
status() {
    print_header "Estado de los servicios"
    
    check_docker
    
    docker-compose -f "$DOCKER_COMPOSE_FILE" ps
    
    print_info "Health checks:"
    docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -E "healthy|unhealthy|starting" || true
}

# Actualizar código
update() {
    print_header "Actualizando código"
    
    print_info "Deteniendo servicios..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down
    
    print_info "Reconstruyendo imagen..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache
    
    print_info "Iniciando servicios..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    sleep 5
    status
    
    print_success "Actualización completada"
}

# Limpiar
clean() {
    print_header "Limpiando"
    
    check_docker
    
    print_warning "Esto eliminará todos los contenedores, volúmenes e imágenes"
    read -p "¿Estás seguro? (s/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        print_info "Deteniendo y eliminando contenedores..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" down -v
        
        print_info "Eliminando imágenes..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" down --rmi all
        
        print_success "Limpieza completada"
    else
        print_info "Limpieza cancelada"
    fi
}

# Verificar salud
health() {
    print_header "Verificando salud del servicio"
    
    check_docker
    
    print_info "Realizando health check..."
    
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_success "Servidor MCP está funcionando correctamente"
        curl -s http://localhost:8000/health | python -m json.tool
    else
        print_error "El servidor MCP no está respondiendo"
        exit 1
    fi
}

# Información
info() {
    print_header "Información del Servidor MCP"
    
    print_info "Realizando consulta de información..."
    
    if curl -f http://localhost:8000/info &> /dev/null; then
        curl -s http://localhost:8000/info | python -m json.tool
    else
        print_error "No se puede conectar al servidor"
        exit 1
    fi
}

# Mostrar ayuda
show_help() {
    cat << EOF
${BLUE}Tienda Nube API MCP Server - Script de Deployment${NC}

${YELLOW}Uso:${NC}
    ./deploy.sh [COMANDO]

${YELLOW}Comandos:${NC}
    build       Construir imagen Docker
    start       Iniciar servicios
    stop        Detener servicios
    restart     Reiniciar servicios
    logs        Mostrar logs (opcional: especificar servicio)
    status      Mostrar estado de servicios
    update      Actualizar código y reiniciar
    clean       Limpiar contenedores e imágenes
    health      Verificar salud del servidor
    info        Obtener información del servidor
    help        Mostrar esta ayuda

${YELLOW}Ejemplos:${NC}
    ./deploy.sh start
    ./deploy.sh logs mcp-server
    ./deploy.sh status
    ./deploy.sh restart

${YELLOW}URLs:${NC}
    HTTP:           http://localhost
    HTTPS:          https://localhost
    Documentación:  http://localhost/docs
    API:            http://localhost/api/v1

${YELLOW}Logs:${NC}
    Todos:          ./logs/
    Nginx:          ./logs/nginx/

EOF
}

# Main
main() {
    COMMAND=${1:-"help"}
    
    case "$COMMAND" in
        build)
            build
            ;;
        start)
            start
            ;;
        stop)
            stop
            ;;
        restart)
            restart
            ;;
        logs)
            logs "$2"
            ;;
        status)
            status
            ;;
        update)
            update
            ;;
        clean)
            clean
            ;;
        health)
            health
            ;;
        info)
            info
            ;;
        help)
            show_help
            ;;
        *)
            print_error "Comando desconocido: $COMMAND"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar
main "$@"

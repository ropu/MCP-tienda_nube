#!/bin/bash

################################################################################
# Script de Pruebas Automatizadas para Herramientas MCP
# Prueba todos los 8 endpoints de herramientas MCP
# Incluye casos de éxito, error y rate limiting
################################################################################

set -e

# Configuración
BASE_URL="${1:-http://localhost:8000}"
RESULTS_FILE="test_results_$(date +%Y%m%d_%H%M%S).txt"
PASSED=0
FAILED=0
SKIPPED=0

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# Funciones Auxiliares
################################################################################

log_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
    echo "=== $1 ===" >> "$RESULTS_FILE"
}

log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
    echo "[TEST] $1" >> "$RESULTS_FILE"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    echo "[PASS] $1" >> "$RESULTS_FILE"
    ((PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    echo "[FAIL] $1" >> "$RESULTS_FILE"
    ((FAILED++))
}

log_skip() {
    echo -e "${YELLOW}[SKIP]${NC} $1"
    echo "[SKIP] $1" >> "$RESULTS_FILE"
    ((SKIPPED++))
}

# Función para hacer request y validar respuesta
test_endpoint() {
    local test_id=$1
    local description=$2
    local method=$3
    local endpoint=$4
    local expected_code=$5
    local validate_json=${6:-true}
    
    log_test "$test_id: $description"
    
    # Hacer request
    local response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint")
    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | head -n-1)
    
    # Validar código HTTP
    if [ "$http_code" = "$expected_code" ]; then
        if [ "$validate_json" = "true" ]; then
            # Validar JSON
            if echo "$body" | python3 -m json.tool > /dev/null 2>&1; then
                log_pass "$test_id: HTTP $http_code, JSON válido"
            else
                log_fail "$test_id: HTTP $http_code, JSON inválido"
            fi
        else
            log_pass "$test_id: HTTP $http_code"
        fi
    else
        log_fail "$test_id: HTTP $http_code (esperado $expected_code)"
    fi
}

################################################################################
# Herramienta 1: search_endpoint
################################################################################

test_search_endpoint() {
    log_header "Herramienta 1: search_endpoint"
    
    # Casos de éxito
    test_endpoint "SE-1.1" "Buscar todos los endpoints de productos" \
        "POST" "/tools/search_endpoint?resource=products" "200"
    
    test_endpoint "SE-1.2" "Buscar todos los endpoints de órdenes" \
        "POST" "/tools/search_endpoint?resource=orders" "200"
    
    test_endpoint "SE-1.3" "Buscar endpoints POST de productos" \
        "POST" "/tools/search_endpoint?resource=products&method=POST" "200"
    
    test_endpoint "SE-1.4" "Buscar endpoints GET de órdenes" \
        "POST" "/tools/search_endpoint?resource=orders&method=GET" "200"
    
    test_endpoint "SE-1.5" "Buscar por nombre (create)" \
        "POST" "/tools/search_endpoint?resource=products&query=create" "200"
    
    test_endpoint "SE-1.6" "Buscar por nombre (pay)" \
        "POST" "/tools/search_endpoint?resource=orders&query=pay" "200"
    
    # Casos de error
    test_endpoint "SE-2.1" "Resource faltante" \
        "POST" "/tools/search_endpoint" "400"
    
    test_endpoint "SE-2.2" "Resource inválido" \
        "POST" "/tools/search_endpoint?resource=invalid" "400"
    
    test_endpoint "SE-2.3" "Method inválido" \
        "POST" "/tools/search_endpoint?resource=products&method=INVALID" "400"
    
    # Casos límite
    test_endpoint "SE-3.1" "Query con espacios" \
        "POST" "/tools/search_endpoint?resource=products&query=list%20products" "200"
    
    test_endpoint "SE-3.2" "Query con números" \
        "POST" "/tools/search_endpoint?resource=products&query=123" "200"
}

################################################################################
# Herramienta 2: get_endpoint_details
################################################################################

test_get_endpoint_details() {
    log_header "Herramienta 2: get_endpoint_details"
    
    # Casos de éxito
    test_endpoint "GED-1.1" "GET /products" \
        "POST" "/tools/get_endpoint_details?resource=products&path=/products&method=GET" "200"
    
    test_endpoint "GED-1.2" "POST /products" \
        "POST" "/tools/get_endpoint_details?resource=products&path=/products&method=POST" "200"
    
    test_endpoint "GED-1.3" "PATCH /products/stock-price" \
        "POST" "/tools/get_endpoint_details?resource=products&path=/products/stock-price&method=PATCH" "200"
    
    test_endpoint "GED-1.4" "GET /orders" \
        "POST" "/tools/get_endpoint_details?resource=orders&path=/orders&method=GET" "200"
    
    test_endpoint "GED-1.5" "POST /orders" \
        "POST" "/tools/get_endpoint_details?resource=orders&path=/orders&method=POST" "200"
    
    test_endpoint "GED-1.7" "Sin method (default GET)" \
        "POST" "/tools/get_endpoint_details?resource=products&path=/products" "200"
    
    # Casos de error
    test_endpoint "GED-2.1" "Resource faltante" \
        "POST" "/tools/get_endpoint_details?path=/products" "400"
    
    test_endpoint "GED-2.2" "Path faltante" \
        "POST" "/tools/get_endpoint_details?resource=products" "400"
    
    test_endpoint "GED-2.3" "Resource inválido" \
        "POST" "/tools/get_endpoint_details?resource=invalid&path=/products" "400"
    
    test_endpoint "GED-2.5" "Method inválido" \
        "POST" "/tools/get_endpoint_details?resource=products&path=/products&method=INVALID" "400"
    
    # Casos límite
    test_endpoint "GED-3.2" "Path con guiones" \
        "POST" "/tools/get_endpoint_details?resource=products&path=/products/stock-price" "200"
}

################################################################################
# Herramienta 3: get_schema
################################################################################

test_get_schema() {
    log_header "Herramienta 3: get_schema"
    
    # Casos de éxito
    test_endpoint "GS-1.1" "Schema respuesta productos" \
        "POST" "/tools/get_schema?resource=products&endpoint_type=response" "200"
    
    test_endpoint "GS-1.2" "Schema solicitud productos" \
        "POST" "/tools/get_schema?resource=products&endpoint_type=request" "200"
    
    test_endpoint "GS-1.3" "Schema respuesta órdenes" \
        "POST" "/tools/get_schema?resource=orders&endpoint_type=response" "200"
    
    test_endpoint "GS-1.4" "Schema solicitud órdenes" \
        "POST" "/tools/get_schema?resource=orders&endpoint_type=request" "200"
    
    test_endpoint "GS-1.5" "Sin endpoint_type (default)" \
        "POST" "/tools/get_schema?resource=products" "200"
    
    # Casos de error
    test_endpoint "GS-2.1" "Resource faltante" \
        "POST" "/tools/get_schema?endpoint_type=response" "400"
    
    test_endpoint "GS-2.2" "Resource inválido" \
        "POST" "/tools/get_schema?resource=invalid&endpoint_type=response" "400"
    
    test_endpoint "GS-2.3" "Endpoint_type inválido" \
        "POST" "/tools/get_schema?resource=products&endpoint_type=invalid" "400"
    
    # Casos límite
    test_endpoint "GS-3.3" "Ambos recursos" \
        "POST" "/tools/get_schema?resource=products" "200"
}

################################################################################
# Herramienta 4: search_documentation
################################################################################

test_search_documentation() {
    log_header "Herramienta 4: search_documentation"
    
    # Casos de éxito
    test_endpoint "SD-1.1" "Buscar multi-inventario" \
        "POST" "/tools/search_documentation?query=multi-inventario" "200"
    
    test_endpoint "SD-1.2" "Buscar stock" \
        "POST" "/tools/search_documentation?query=stock" "200"
    
    test_endpoint "SD-1.3" "Buscar pay" \
        "POST" "/tools/search_documentation?query=pay" "200"
    
    test_endpoint "SD-1.4" "Buscar inventory" \
        "POST" "/tools/search_documentation?query=inventory" "200"
    
    test_endpoint "SD-1.5" "Buscar product" \
        "POST" "/tools/search_documentation?query=product" "200"
    
    # Casos de error
    test_endpoint "SD-2.1" "Query faltante" \
        "POST" "/tools/search_documentation" "400"
    
    test_endpoint "SD-2.4" "Query con caracteres especiales" \
        "POST" "/tools/search_documentation?query=%3Cscript%3E" "200"
    
    # Casos límite
    test_endpoint "SD-3.1" "Query con espacios" \
        "POST" "/tools/search_documentation?query=multi%20inventario" "200"
}

################################################################################
# Herramienta 5: get_code_example
################################################################################

test_get_code_example() {
    log_header "Herramienta 5: get_code_example"
    
    # Casos de éxito
    test_endpoint "GCE-1.1" "Python GET /products" \
        "POST" "/tools/get_code_example?resource=products&path=/products&language=python" "200"
    
    test_endpoint "GCE-1.2" "Python POST /products" \
        "POST" "/tools/get_code_example?resource=products&path=/products&method=POST&language=python" "200"
    
    test_endpoint "GCE-1.3" "JavaScript GET /products" \
        "POST" "/tools/get_code_example?resource=products&path=/products&language=javascript" "200"
    
    test_endpoint "GCE-1.4" "JavaScript POST /products" \
        "POST" "/tools/get_code_example?resource=products&path=/products&method=POST&language=javascript" "200"
    
    test_endpoint "GCE-1.7" "Sin language (default Python)" \
        "POST" "/tools/get_code_example?resource=products&path=/products" "200"
    
    test_endpoint "GCE-1.8" "Sin method (default GET)" \
        "POST" "/tools/get_code_example?resource=products&path=/products&language=python" "200"
    
    # Casos de error
    test_endpoint "GCE-2.1" "Resource faltante" \
        "POST" "/tools/get_code_example?path=/products&language=python" "400"
    
    test_endpoint "GCE-2.2" "Path faltante" \
        "POST" "/tools/get_code_example?resource=products&language=python" "400"
    
    test_endpoint "GCE-2.5" "Language inválido" \
        "POST" "/tools/get_code_example?resource=products&path=/products&language=ruby" "400"
    
    test_endpoint "GCE-2.6" "Method inválido" \
        "POST" "/tools/get_code_example?resource=products&path=/products&method=INVALID&language=python" "400"
}

################################################################################
# Herramientas 6-8: Sin parámetros
################################################################################

test_no_params_tools() {
    log_header "Herramientas sin parámetros"
    
    # get_authentication_info
    test_endpoint "GAI-1.1" "Obtener info autenticación" \
        "POST" "/tools/get_authentication_info" "200"
    
    test_endpoint "GAI-1.3" "Múltiples llamadas consecutivas" \
        "POST" "/tools/get_authentication_info" "200"
    
    # get_multi_inventory_info
    test_endpoint "GMI-1.1" "Obtener info multi-inventario" \
        "POST" "/tools/get_multi_inventory_info" "200"
    
    # list_resources
    test_endpoint "LR-1.1" "Listar recursos" \
        "POST" "/tools/list_resources" "200"
}

################################################################################
# Pruebas de Rate Limiting
################################################################################

test_rate_limiting() {
    log_header "Pruebas de Rate Limiting"
    
    log_test "RL-1: Prueba de rate limiting (10 req/s)"
    
    local endpoint="/tools/search_endpoint?resource=products"
    local count=0
    local success=0
    local rate_limited=0
    
    for i in {1..15}; do
        local response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint")
        local http_code=$(echo "$response" | tail -n1)
        
        if [ "$http_code" = "200" ]; then
            ((success++))
        elif [ "$http_code" = "429" ]; then
            ((rate_limited++))
        fi
        ((count++))
    done
    
    if [ $rate_limited -gt 0 ]; then
        log_pass "RL-1: Rate limiting funcionando (200: $success, 429: $rate_limited)"
    else
        log_fail "RL-1: Rate limiting no detectado"
    fi
}

################################################################################
# Pruebas de Validación de JSON
################################################################################

test_json_validation() {
    log_header "Validación de Respuestas JSON"
    
    log_test "JSON-1: Validar estructura search_endpoint"
    local response=$(curl -s -X POST "$BASE_URL/tools/search_endpoint?resource=products")
    
    if echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); assert 'result' in data or 'tool' in data" 2>/dev/null; then
        log_pass "JSON-1: Estructura válida"
    else
        log_fail "JSON-1: Estructura inválida"
    fi
    
    log_test "JSON-2: Validar estructura get_schema"
    local response=$(curl -s -X POST "$BASE_URL/tools/get_schema?resource=products")
    
    if echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); assert 'result' in data or 'tool' in data" 2>/dev/null; then
        log_pass "JSON-2: Estructura válida"
    else
        log_fail "JSON-2: Estructura inválida"
    fi
}

################################################################################
# Pruebas de Rendimiento
################################################################################

test_performance() {
    log_header "Pruebas de Rendimiento"
    
    log_test "PERF-1: Tiempo de respuesta search_endpoint"
    
    local start_time=$(date +%s%N)
    curl -s -X POST "$BASE_URL/tools/search_endpoint?resource=products" > /dev/null
    local end_time=$(date +%s%N)
    local duration=$((($end_time - $start_time) / 1000000))
    
    if [ $duration -lt 500 ]; then
        log_pass "PERF-1: Tiempo de respuesta ${duration}ms (< 500ms)"
    else
        log_fail "PERF-1: Tiempo de respuesta ${duration}ms (> 500ms)"
    fi
}

################################################################################
# Main
################################################################################

main() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  Suite de Pruebas - Herramientas MCP de Tienda Nube API       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Base URL: $BASE_URL"
    echo "Archivo de resultados: $RESULTS_FILE"
    echo ""
    
    # Verificar que el servidor está disponible
    if ! curl -s "$BASE_URL/health" > /dev/null 2>&1; then
        echo -e "${RED}Error: No se puede conectar a $BASE_URL${NC}"
        exit 1
    fi
    
    # Ejecutar pruebas
    test_search_endpoint
    test_get_endpoint_details
    test_get_schema
    test_search_documentation
    test_get_code_example
    test_no_params_tools
    test_rate_limiting
    test_json_validation
    test_performance
    
    # Resumen
    log_header "RESUMEN DE RESULTADOS"
    
    local total=$((PASSED + FAILED + SKIPPED))
    local pass_rate=$((PASSED * 100 / total))
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    RESUMEN DE PRUEBAS                          ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo -e "║ ${GREEN}Pasadas:${NC}  $PASSED"
    echo -e "║ ${RED}Fallidas:${NC}  $FAILED"
    echo -e "║ ${YELLOW}Omitidas:${NC}  $SKIPPED"
    echo "║ Total:    $total"
    echo -e "║ Tasa de éxito: ${GREEN}${pass_rate}%${NC}"
    echo "╚════════════════════════════════════════════════════════════════╝"
    
    echo ""
    echo "Resultados guardados en: $RESULTS_FILE"
    
    # Retornar código de salida
    if [ $FAILED -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Ejecutar main
main "$@"

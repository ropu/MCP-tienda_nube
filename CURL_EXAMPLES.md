# Ejemplos de Curl - Todos los Endpoints REST

## 🏥 Health & Readiness

### Health Check
```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "service": "tiendanube-api-mcp",
  "version": "1.0.0"
}
```

### Readiness Check
```bash
curl http://localhost:8000/ready
```

**Respuesta:**
```json
{
  "ready": true,
  "resources": {
    "products": 7,
    "orders": 10
  },
  "total_endpoints": 17
}
```

---

## 🛠️ Herramientas MCP

### 1. Search Endpoint - Todos los productos
```bash
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products"
```

### 2. Search Endpoint - Solo POST
```bash
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products&method=POST"
```

### 3. Search Endpoint - Buscar por nombre
```bash
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products&query=create"
```

### 4. Search Endpoint - Órdenes
```bash
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=orders"
```

### 5. Search Endpoint - Órdenes con método DELETE
```bash
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=orders&method=DELETE"
```

---

### 6. Get Endpoint Details - GET /products
```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products&method=GET"
```

### 7. Get Endpoint Details - POST /products
```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products&method=POST"
```

### 8. Get Endpoint Details - PATCH /products/stock-price
```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products/stock-price&method=PATCH"
```

### 9. Get Endpoint Details - GET /orders
```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=orders&path=/orders&method=GET"
```

### 10. Get Endpoint Details - POST /orders
```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=orders&path=/orders&method=POST"
```

### 11. Get Endpoint Details - POST /orders/{id}/pay
```bash
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=orders&path=/orders/{id}/pay&method=POST"
```

---

### 12. Get Schema - Respuesta de productos
```bash
curl -X POST "http://localhost:8000/tools/get_schema?resource=products&endpoint_type=response"
```

### 13. Get Schema - Solicitud de productos
```bash
curl -X POST "http://localhost:8000/tools/get_schema?resource=products&endpoint_type=request"
```

### 14. Get Schema - Respuesta de órdenes
```bash
curl -X POST "http://localhost:8000/tools/get_schema?resource=orders&endpoint_type=response"
```

### 15. Get Schema - Solicitud de órdenes
```bash
curl -X POST "http://localhost:8000/tools/get_schema?resource=orders&endpoint_type=request"
```

---

### 16. Search Documentation - Multi-inventario
```bash
curl -X POST "http://localhost:8000/tools/search_documentation?query=multi-inventario"
```

### 17. Search Documentation - Stock
```bash
curl -X POST "http://localhost:8000/tools/search_documentation?query=stock"
```

### 18. Search Documentation - Pago
```bash
curl -X POST "http://localhost:8000/tools/search_documentation?query=pay"
```

### 19. Search Documentation - Inventario
```bash
curl -X POST "http://localhost:8000/tools/search_documentation?query=inventory"
```

---

### 20. Get Code Example - Python GET /products
```bash
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products&method=GET&language=python"
```

### 21. Get Code Example - Python POST /products
```bash
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products&method=POST&language=python"
```

### 22. Get Code Example - JavaScript GET /products
```bash
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products&method=GET&language=javascript"
```

### 23. Get Code Example - Python PATCH /products/stock-price
```bash
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products/stock-price&method=PATCH&language=python"
```

### 24. Get Code Example - Python GET /orders
```bash
curl -X POST "http://localhost:8000/tools/get_code_example?resource=orders&path=/orders&method=GET&language=python"
```

### 25. Get Code Example - Python POST /orders
```bash
curl -X POST "http://localhost:8000/tools/get_code_example?resource=orders&path=/orders&method=POST&language=python"
```

### 26. Get Code Example - Python POST /orders/{id}/pay
```bash
curl -X POST "http://localhost:8000/tools/get_code_example?resource=orders&path=/orders/{id}/pay&method=POST&language=python"
```

---

### 27. Get Authentication Info
```bash
curl -X POST "http://localhost:8000/tools/get_authentication_info"
```

### 28. Get Multi-Inventory Info
```bash
curl -X POST "http://localhost:8000/tools/get_multi_inventory_info"
```

### 29. List Resources
```bash
curl -X POST "http://localhost:8000/tools/list_resources"
```

---

## ℹ️ Información

### 30. Root
```bash
curl http://localhost:8000/
```

### 31. Info
```bash
curl http://localhost:8000/info
```

### 32. Get All Endpoints
```bash
curl http://localhost:8000/endpoints
```

### 33. Get All Endpoints - Solo productos
```bash
curl http://localhost:8000/endpoints?resource=products
```

### 34. Get All Endpoints - Solo órdenes
```bash
curl http://localhost:8000/endpoints?resource=orders
```

### 35. Get Tools
```bash
curl http://localhost:8000/tools
```

### 36. OpenAPI Schema
```bash
curl http://localhost:8000/openapi.json
```

---

## 🎯 Casos de Uso Completos

### Caso 1: Crear un Producto

```bash
#!/bin/bash

# 1. Buscar endpoint de creación
echo "=== Buscando endpoint de creación ==="
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products&method=POST" | python -m json.tool

# 2. Obtener detalles
echo -e "\n=== Detalles del endpoint ==="
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products&method=POST" | python -m json.tool

# 3. Obtener esquema de solicitud
echo -e "\n=== Esquema de solicitud ==="
curl -X POST "http://localhost:8000/tools/get_schema?resource=products&endpoint_type=request" | python -m json.tool

# 4. Obtener ejemplo de código
echo -e "\n=== Ejemplo de código Python ==="
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products&method=POST&language=python" | python -m json.tool
```

### Caso 2: Actualizar Stock con Multi-Inventario

```bash
#!/bin/bash

# 1. Información de multi-inventario
echo "=== Información de multi-inventario ==="
curl -X POST "http://localhost:8000/tools/get_multi_inventory_info" | python -m json.tool

# 2. Buscar documentación sobre stock
echo -e "\n=== Documentación sobre stock ==="
curl -X POST "http://localhost:8000/tools/search_documentation?query=stock" | python -m json.tool

# 3. Detalles del endpoint de actualización
echo -e "\n=== Detalles de PATCH /products/stock-price ==="
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=products&path=/products/stock-price&method=PATCH" | python -m json.tool

# 4. Ejemplo de código
echo -e "\n=== Ejemplo de código ==="
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products/stock-price&method=PATCH&language=python" | python -m json.tool
```

### Caso 3: Obtener y Pagar Órdenes

```bash
#!/bin/bash

# 1. Listar todos los endpoints de órdenes
echo "=== Endpoints de órdenes ==="
curl http://localhost:8000/endpoints?resource=orders | python -m json.tool

# 2. Detalles de GET /orders
echo -e "\n=== Detalles de GET /orders ==="
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=orders&path=/orders&method=GET" | python -m json.tool

# 3. Detalles de POST /orders/{id}/pay
echo -e "\n=== Detalles de POST /orders/{id}/pay ==="
curl -X POST "http://localhost:8000/tools/get_endpoint_details?resource=orders&path=/orders/{id}/pay&method=POST" | python -m json.tool

# 4. Ejemplos de código
echo -e "\n=== Ejemplo Python para obtener órdenes ==="
curl -X POST "http://localhost:8000/tools/get_code_example?resource=orders&path=/orders&method=GET&language=python" | python -m json.tool

echo -e "\n=== Ejemplo Python para pagar orden ==="
curl -X POST "http://localhost:8000/tools/get_code_example?resource=orders&path=/orders/{id}/pay&method=POST&language=python" | python -m json.tool
```

---

## 📊 Monitoreo

### Verificar Salud
```bash
#!/bin/bash

echo "=== Health Check ==="
curl http://localhost:8000/health | python -m json.tool

echo -e "\n=== Readiness Check ==="
curl http://localhost:8000/ready | python -m json.tool

echo -e "\n=== Información del Servidor ==="
curl http://localhost:8000/info | python -m json.tool
```

---

## 🔄 Scripting con Curl

### Script Python para Explorar Toda la API

```python
#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def make_request(method, endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    if method == "GET":
        response = requests.get(url, params=params)
    else:
        response = requests.post(url, params=params)
    return response.json()

# Health
print_section("Health Check")
print(json.dumps(make_request("GET", "/health"), indent=2))

# Info
print_section("Server Info")
print(json.dumps(make_request("GET", "/info"), indent=2))

# Search endpoints
print_section("Search Endpoints - Products")
result = make_request("POST", "/tools/search_endpoint", {"resource": "products"})
print(json.dumps(result, indent=2))

# Get details
print_section("Endpoint Details - POST /products")
result = make_request("POST", "/tools/get_endpoint_details", {
    "resource": "products",
    "path": "/products",
    "method": "POST"
})
print(json.dumps(result, indent=2))

# Code example
print_section("Code Example - Python")
result = make_request("POST", "/tools/get_code_example", {
    "resource": "products",
    "path": "/products",
    "method": "POST",
    "language": "python"
})
print(result["result"])

# Multi-inventory
print_section("Multi-Inventory Info")
result = make_request("POST", "/tools/get_multi_inventory_info")
print(json.dumps(result, indent=2))
```

---

## 🧪 Testing con Curl

### Test de Todos los Endpoints

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"
PASSED=0
FAILED=0

test_endpoint() {
    local method=$1
    local endpoint=$2
    local params=$3
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint$params")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "200" ]; then
        echo "✓ $method $endpoint"
        ((PASSED++))
    else
        echo "✗ $method $endpoint (HTTP $http_code)"
        ((FAILED++))
    fi
}

echo "Testing all endpoints..."

# Health
test_endpoint "GET" "/health"
test_endpoint "GET" "/ready"

# Tools
test_endpoint "POST" "/tools/search_endpoint" "?resource=products"
test_endpoint "POST" "/tools/get_endpoint_details" "?resource=products&path=/products"
test_endpoint "POST" "/tools/get_schema" "?resource=products"
test_endpoint "POST" "/tools/search_documentation" "?query=stock"
test_endpoint "POST" "/tools/get_code_example" "?resource=products&path=/products&language=python"
test_endpoint "POST" "/tools/get_authentication_info"
test_endpoint "POST" "/tools/get_multi_inventory_info"
test_endpoint "POST" "/tools/list_resources"

# Info
test_endpoint "GET" "/"
test_endpoint "GET" "/info"
test_endpoint "GET" "/endpoints"
test_endpoint "GET" "/tools"
test_endpoint "GET" "/openapi.json"
test_endpoint "GET" "/docs"
test_endpoint "GET" "/redoc"

echo -e "\n=== Resultados ==="
echo "Pasadas: $PASSED"
echo "Fallidas: $FAILED"
echo "Total: $((PASSED + FAILED))"
```

---

## 📈 Benchmarking

### Medir Latencia

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

benchmark_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    
    echo "Benchmarking $method $endpoint..."
    
    for i in {1..10}; do
        time curl -s -X $method "$BASE_URL$endpoint" > /dev/null
    done
}

benchmark_endpoint "/health"
benchmark_endpoint "/info"
benchmark_endpoint "/tools/search_endpoint?resource=products" "POST"
```

---

## 🔗 Integración con Herramientas

### Usar con jq para Procesar JSON

```bash
# Obtener solo nombres de endpoints
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products" | jq '.result[].name'

# Obtener solo métodos HTTP
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products" | jq '.result[].method'

# Contar endpoints
curl http://localhost:8000/endpoints | jq '.total'

# Obtener información de autenticación
curl -X POST "http://localhost:8000/tools/get_authentication_info" | jq '.result.scopes'
```

### Usar con grep y awk

```bash
# Buscar endpoints POST
curl http://localhost:8000/endpoints | grep -i '"POST"'

# Contar endpoints por tipo
curl http://localhost:8000/endpoints | grep -o '"method": "[^"]*"' | sort | uniq -c
```

---

**Versión**: 1.0.0  
**Última actualización**: 2025-01-04  
**Total Ejemplos**: 36+

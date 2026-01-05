# Guía de Ejecución de Pruebas - Herramientas MCP

## 📋 Resumen

Este documento describe cómo ejecutar las pruebas exhaustivas para los 8 endpoints de herramientas MCP del servidor FastAPI.

**Total de Casos de Prueba:** 158
- Casos de Éxito: 47
- Casos de Error: 54
- Casos de Rate Limiting: 24
- Casos Límite: 33

---

## 🚀 Requisitos Previos

### 1. Servidor MCP Corriendo

```bash
# Iniciar el servidor
cd /home/ubuntu/tiendanube_mcp
make start

# O con docker-compose
docker-compose up -d

# Verificar que está corriendo
curl http://localhost:8000/health
```

### 2. Instalar Dependencias de Prueba

```bash
# Instalar pytest, requests y locust
pip install pytest requests locust

# O usando requirements
pip install -r requirements.txt
```

---

## 🧪 Métodos de Prueba

### Método 1: Script Bash (Pruebas Rápidas)

**Archivo:** `test_mcp_tools.sh`

**Ventajas:**
- No requiere dependencias Python adicionales
- Rápido y fácil de ejecutar
- Genera reporte de resultados

**Ejecución:**

```bash
# Hacer ejecutable
chmod +x test_mcp_tools.sh

# Ejecutar con servidor en localhost:8000
./test_mcp_tools.sh

# Ejecutar con servidor en otro host
./test_mcp_tools.sh http://192.168.1.100:8000

# Ver resultados
cat test_results_*.txt
```

**Salida Esperada:**

```
╔════════════════════════════════════════════════════════════════╗
║  Suite de Pruebas - Herramientas MCP de Tienda Nube API       ║
╚════════════════════════════════════════════════════════════════╝

Base URL: http://localhost:8000
Archivo de resultados: test_results_20250104_120000.txt

[TEST] SE-1.1: Buscar todos los endpoints de productos
[PASS] SE-1.1: HTTP 200, JSON válido
...

╔════════════════════════════════════════════════════════════════╗
║                    RESUMEN DE PRUEBAS                          ║
╠════════════════════════════════════════════════════════════════╣
║ Pasadas:  45
║ Fallidas:  2
║ Omitidas:  0
║ Total:    47
║ Tasa de éxito: 95%
╚════════════════════════════════════════════════════════════════╝
```

---

### Método 2: Pytest (Pruebas Completas)

**Archivo:** `test_mcp_pytest.py`

**Ventajas:**
- Pruebas organizadas por clase
- Mejor reporte de errores
- Fácil de integrar en CI/CD

**Ejecución:**

```bash
# Ejecutar todas las pruebas
pytest test_mcp_pytest.py -v

# Ejecutar pruebas de una clase específica
pytest test_mcp_pytest.py::TestSearchEndpoint -v

# Ejecutar una prueba específica
pytest test_mcp_pytest.py::TestSearchEndpoint::test_se_1_1_search_all_products -v

# Ejecutar con reporte HTML
pytest test_mcp_pytest.py -v --html=report.html

# Ejecutar con cobertura
pytest test_mcp_pytest.py --cov=. --cov-report=html

# Ejecutar solo pruebas de éxito
pytest test_mcp_pytest.py -k "test_.*_1_" -v

# Ejecutar solo pruebas de error
pytest test_mcp_pytest.py -k "test_.*_2_" -v

# Ejecutar solo pruebas de rendimiento
pytest test_mcp_pytest.py::TestPerformance -v
```

**Salida Esperada:**

```
test_mcp_pytest.py::TestSearchEndpoint::test_se_1_1_search_all_products PASSED
test_mcp_pytest.py::TestSearchEndpoint::test_se_1_2_search_all_orders PASSED
test_mcp_pytest.py::TestSearchEndpoint::test_se_1_3_search_post_products PASSED
...

============================== 95 passed in 12.34s ==============================
```

---

### Método 3: Pruebas de Rate Limiting

**Archivo:** `test_rate_limiting.py`

**Ventajas:**
- Pruebas específicas de límites
- Simula diferentes patrones de carga
- Valida recuperación

**Ejecución:**

```bash
# Ejecutar todas las pruebas de rate limiting
python test_rate_limiting.py

# Ejecutar con Locust (pruebas de carga)
locust -f test_rate_limiting.py --host=http://localhost:8000 --users 10 --spawn-rate 2
```

**Salida Esperada:**

```
======================================================================
Prueba: 5 solicitudes por segundo (dentro del límite)
======================================================================

  [1/5] ✓ HTTP 200 (45.2ms)
  [2/5] ✓ HTTP 200 (42.1ms)
  [3/5] ✓ HTTP 200 (43.8ms)
  [4/5] ✓ HTTP 200 (44.5ms)
  [5/5] ✓ HTTP 200 (43.9ms)

Resultado: 5/5 exitosas

======================================================================
Prueba: 15 solicitudes por segundo (excediendo el límite)
======================================================================

  [ 1/15] ✓ HTTP 200 (45.2ms)
  [ 2/15] ✓ HTTP 200 (42.1ms)
  [ 3/15] ⚠ HTTP 429 (Rate Limited)
  ...
  [15/15] ⚠ HTTP 429 (Rate Limited)

Resultado: 10/15 exitosas, 5 limitadas

======================================================================
ESTADÍSTICAS DE RATE LIMITING
======================================================================

Tiempos de Respuesta:
  Promedio: 43.5ms
  Mínimo:   41.2ms
  Máximo:   125.3ms

Resultados Generales:
  Exitosas:    45
  Limitadas:   15
  Errores:     0
  Tasa de éxito: 75.0%
```

---

## 📊 Casos de Prueba por Herramienta

### Herramienta 1: search_endpoint (22 casos)

```bash
# Ejecutar solo pruebas de search_endpoint
pytest test_mcp_pytest.py::TestSearchEndpoint -v
```

**Casos:**
- 6 casos de éxito
- 8 casos de error
- 3 casos de rate limiting
- 5 casos límite

---

### Herramienta 2: get_endpoint_details (27 casos)

```bash
# Ejecutar solo pruebas de get_endpoint_details
pytest test_mcp_pytest.py::TestGetEndpointDetails -v
```

**Casos:**
- 8 casos de éxito
- 10 casos de error
- 3 casos de rate limiting
- 6 casos límite

---

### Herramienta 3: get_schema (20 casos)

```bash
# Ejecutar solo pruebas de get_schema
pytest test_mcp_pytest.py::TestGetSchema -v
```

**Casos:**
- 6 casos de éxito
- 7 casos de error
- 3 casos de rate limiting
- 4 casos límite

---

### Herramienta 4: search_documentation (25 casos)

```bash
# Ejecutar solo pruebas de search_documentation
pytest test_mcp_pytest.py::TestSearchDocumentation -v
```

**Casos:**
- 8 casos de éxito
- 8 casos de error
- 3 casos de rate limiting
- 6 casos límite

---

### Herramienta 5: get_code_example (31 casos)

```bash
# Ejecutar solo pruebas de get_code_example
pytest test_mcp_pytest.py::TestGetCodeExample -v
```

**Casos:**
- 10 casos de éxito
- 12 casos de error
- 3 casos de rate limiting
- 6 casos límite

---

### Herramientas 6-8: Sin Parámetros (11 casos cada una)

```bash
# Ejecutar solo pruebas de herramientas sin parámetros
pytest test_mcp_pytest.py::TestNoParamsTools -v
```

**Casos por herramienta:**
- 3 casos de éxito
- 3 casos de error
- 3 casos de rate limiting
- 2 casos límite

---

## 🔍 Validaciones Específicas

### Validar Respuestas JSON

```bash
# Ejecutar solo pruebas de validación JSON
pytest test_mcp_pytest.py::TestJSONValidation -v
```

**Valida:**
- JSON válido y bien formado
- Estructura correcta
- Campos requeridos presentes

---

### Validar Rendimiento

```bash
# Ejecutar solo pruebas de rendimiento
pytest test_mcp_pytest.py::TestPerformance -v
```

**Valida:**
- Tiempo de respuesta < 500ms
- Consistencia en tiempos

---

## 📈 Pruebas de Carga

### Con Apache Bench

```bash
# 1000 solicitudes, 10 concurrentes
ab -n 1000 -c 10 http://localhost:8000/tools/search_endpoint?resource=products

# 5000 solicitudes, 50 concurrentes
ab -n 5000 -c 50 http://localhost:8000/tools/search_endpoint?resource=products
```

### Con Locust

```bash
# Interfaz web
locust -f test_rate_limiting.py --host=http://localhost:8000

# Línea de comandos
locust -f test_rate_limiting.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 60s --headless
```

---

## 🛠️ Comandos Útiles

### Ejecutar Todas las Pruebas

```bash
# Bash
./test_mcp_tools.sh

# Pytest
pytest test_mcp_pytest.py -v

# Ambas
./test_mcp_tools.sh && pytest test_mcp_pytest.py -v
```

### Generar Reportes

```bash
# Reporte HTML con pytest
pytest test_mcp_pytest.py -v --html=report.html --self-contained-html

# Reporte con cobertura
pytest test_mcp_pytest.py --cov=. --cov-report=html --cov-report=term

# Reporte JUnit XML
pytest test_mcp_pytest.py -v --junit-xml=report.xml
```

### Ejecutar Pruebas Específicas

```bash
# Solo casos de éxito
pytest test_mcp_pytest.py -k "test_.*_1_" -v

# Solo casos de error
pytest test_mcp_pytest.py -k "test_.*_2_" -v

# Solo casos límite
pytest test_mcp_pytest.py -k "test_.*_3_" -v

# Solo rate limiting
pytest test_mcp_pytest.py -k "test_rate" -v

# Solo una herramienta
pytest test_mcp_pytest.py::TestSearchEndpoint -v
```

### Ejecutar en Paralelo

```bash
# Instalar pytest-xdist
pip install pytest-xdist

# Ejecutar con 4 workers
pytest test_mcp_pytest.py -v -n 4
```

---

## 📋 Checklist de Pruebas

### Antes de Ejecutar

- [ ] Servidor MCP corriendo en http://localhost:8000
- [ ] Dependencias instaladas (pytest, requests, locust)
- [ ] Base de datos de API cargada
- [ ] Health check pasando (`curl http://localhost:8000/health`)

### Durante la Ejecución

- [ ] Monitorear logs del servidor
- [ ] Verificar uso de CPU y memoria
- [ ] Anotar cualquier comportamiento inusual

### Después de Ejecutar

- [ ] Revisar reporte de resultados
- [ ] Documentar fallos
- [ ] Crear issues si hay problemas
- [ ] Archivar resultados para referencia

---

## 🐛 Troubleshooting

### Error: Connection refused

```
Error: No se puede conectar a http://localhost:8000
```

**Solución:**
```bash
# Verificar que el servidor está corriendo
curl http://localhost:8000/health

# Si no está corriendo, iniciar
make start
```

### Error: Timeout

```
Error: Timeout esperando respuesta
```

**Solución:**
```bash
# Aumentar timeout en scripts
# En test_mcp_pytest.py, cambiar TIMEOUT = 10 a TIMEOUT = 30

# O ejecutar con menos concurrencia
pytest test_mcp_pytest.py -v -n 1
```

### Error: Rate limiting no detectado

```
Error: Prueba de rate limiting fallida
```

**Solución:**
```bash
# Verificar configuración de rate limiting en nginx.conf
# Verificar que Nginx está corriendo
docker ps | grep nginx

# Revisar logs de Nginx
docker logs tiendanube-mcp-nginx
```

### Error: JSON inválido

```
Error: JSON parsing error
```

**Solución:**
```bash
# Verificar respuesta manualmente
curl -s http://localhost:8000/tools/search_endpoint?resource=products | python -m json.tool

# Si hay error, revisar logs del servidor
docker logs tiendanube-mcp-server
```

---

## 📊 Interpretación de Resultados

### Tasa de Éxito

| Tasa | Interpretación |
|------|---|
| 100% | ✓ Perfecto - Todos los tests pasan |
| 95-99% | ✓ Excelente - Fallos menores |
| 90-94% | ⚠ Bueno - Revisar fallos |
| 80-89% | ⚠ Aceptable - Investigar problemas |
| <80% | ✗ Crítico - Resolver antes de producción |

### Tiempo de Respuesta

| Tiempo | Interpretación |
|--------|---|
| <100ms | ✓ Excelente |
| 100-200ms | ✓ Bueno |
| 200-500ms | ⚠ Aceptable |
| >500ms | ✗ Lento - Investigar |

### Rate Limiting

| Comportamiento | Esperado |
|---|---|
| 0-10 req/s | ✓ Todas exitosas |
| 10-15 req/s | ⚠ Algunas limitadas |
| >15 req/s | ✓ Mayoría limitadas |

---

## 📝 Documentación de Resultados

### Formato de Reporte

```
Fecha: 2025-01-04
Hora: 12:00:00
Servidor: http://localhost:8000
Versión: 1.0.0

RESUMEN:
  Total Casos: 158
  Pasadas: 150
  Fallidas: 8
  Omitidas: 0
  Tasa de Éxito: 94.9%

DETALLES POR HERRAMIENTA:
  search_endpoint: 21/22 (95.5%)
  get_endpoint_details: 26/27 (96.3%)
  get_schema: 20/20 (100%)
  search_documentation: 24/25 (96%)
  get_code_example: 30/31 (96.8%)
  get_authentication_info: 11/11 (100%)
  get_multi_inventory_info: 11/11 (100%)
  list_resources: 11/11 (100%)

FALLOS:
  - SE-2.4: Query vacío (esperado 400, obtuvo 200)
  - GED-2.4: Path inválido (esperado 404, obtuvo 200)
  ...

RECOMENDACIONES:
  - Revisar validación de parámetros
  - Mejorar manejo de errores
  - Optimizar rendimiento
```

---

## 🚀 Integración en CI/CD

### GitHub Actions

```yaml
name: Test MCP Tools

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install pytest requests locust
    
    - name: Start server
      run: |
        docker-compose up -d
        sleep 5
    
    - name: Run tests
      run: |
        pytest test_mcp_pytest.py -v --junit-xml=report.xml
    
    - name: Upload report
      uses: actions/upload-artifact@v2
      if: always()
      with:
        name: test-report
        path: report.xml
```

---

**Versión:** 1.0.0  
**Última actualización:** 2025-01-04  
**Total Casos de Prueba:** 158

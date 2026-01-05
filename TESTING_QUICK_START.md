# Quick Start - Pruebas en 5 Minutos

## 🚀 Inicio Rápido

### Paso 1: Instalar Dependencias (1 min)

```bash
pip install pytest requests
```

### Paso 2: Iniciar Servidor (1 min)

```bash
cd /home/ubuntu/tiendanube_mcp
make start
# O: docker-compose up -d
```

### Paso 3: Ejecutar Pruebas (3 min)

**Opción A: Script Bash (Más Rápido)**
```bash
./test_mcp_tools.sh
```

**Opción B: Pytest (Más Detallado)**
```bash
pytest test_mcp_pytest.py -v
```

---

## ✅ Resultado Esperado

```
╔════════════════════════════════════════════════════════════════╗
║                    RESUMEN DE PRUEBAS                          ║
╠════════════════════════════════════════════════════════════════╣
║ Pasadas:  45+
║ Fallidas:  0
║ Total:    45+
║ Tasa de éxito: 100%
╚════════════════════════════════════════════════════════════════╝
```

---

## 🔍 Validar Manualmente

```bash
# Health check
curl http://localhost:8000/health

# Buscar endpoints
curl -X POST "http://localhost:8000/tools/search_endpoint?resource=products"

# Obtener código ejemplo
curl -X POST "http://localhost:8000/tools/get_code_example?resource=products&path=/products&language=python"
```

---

## 📊 Ver Resultados Detallados

```bash
# Reporte bash
cat test_results_*.txt

# Reporte pytest
pytest test_mcp_pytest.py -v --html=report.html
```

---

## 🆘 Si Algo Falla

```bash
# Verificar servidor
curl http://localhost:8000/health

# Ver logs
docker logs tiendanube-mcp-server

# Reiniciar
make restart
```

---

**¡Listo! Pruebas completadas en 5 minutos.** ✅

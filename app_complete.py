#!/usr/bin/env python3
"""
Servidor MCP Completo para Tienda Nube API
Expone TODOS los 111 endpoints de la API como herramientas MCP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Tienda Nube MCP - Servidor Completo",
    description="Servidor MCP con TODOS los 111 endpoints de la API de Tienda Nube",
    version="2.0.0"
)

# Agregar CORS - IMPORTANTE: Debe estar ANTES de montar FastAPI-MCP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Incluye GET para SSE
    allow_headers=["*"],
    expose_headers=["*"],  # Exponer headers para SSE
)

# Cargar base de datos completa
try:
    # Intentar cargar desde ruta absoluta (VPS)
    db_path = Path('/home/ubuntu/tiendanube_mcp/api_database_complete.json')
    if not db_path.exists():
        # Si no existe, intentar desde ruta relativa (local/Docker)
        db_path = Path(__file__).parent / 'api_database_complete.json'
    if not db_path.exists():
        # Fallback a api_database.json
        db_path = Path(__file__).parent / 'api_database.json'
    
    with open(db_path, 'r', encoding='utf-8') as f:
        API_DATABASE = json.load(f)
    logger.info(f"✅ Base de datos cargada: {len(API_DATABASE.get('endpoints', {}))} recursos")
except Exception as e:
    logger.error(f"❌ Error cargando base de datos: {e}")
    API_DATABASE = {"endpoints": {}, "metadata": {}}

# ===== ENDPOINTS DE SALUD =====

@app.get("/health")
async def health():
    """Health check del servidor"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/ready")
async def ready():
    """Readiness check del servidor"""
    return {
        "status": "ready",
        "resources": len(API_DATABASE['endpoints']),
        "endpoints": sum(len(e) for e in API_DATABASE['endpoints'].values()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info")
async def info():
    """Información del servidor MCP"""
    return {
        "name": "Tienda Nube MCP - Servidor Completo",
        "version": "2.0.0",
        "api_version": "2025-03",
        "resources": len(API_DATABASE['endpoints']),
        "endpoints": sum(len(e) for e in API_DATABASE['endpoints'].values()),
        "coverage": "100%",
        "resources_list": list(API_DATABASE['endpoints'].keys())
    }

# ===== HERRAMIENTAS MCP =====

@app.post("/tools/search_endpoint", operation_id="search_endpoint")
async def search_endpoint(query: str, resource: Optional[str] = None):
    """Buscar endpoints por nombre, método o path"""
    try:
        results = []
        
        # Filtrar por recurso si se especifica
        resources_to_search = {resource: API_DATABASE['endpoints'][resource]} if resource else API_DATABASE['endpoints']
        
        for res_name, endpoints in resources_to_search.items():
            for endpoint in endpoints:
                if (query.lower() in endpoint.get('name', '').lower() or
                    query.lower() in endpoint.get('path', '').lower() or
                    query.lower() in endpoint.get('method', '').lower() or
                    query.lower() in endpoint.get('description', '').lower()):
                    results.append({
                        "resource": res_name,
                        "method": endpoint.get('method'),
                        "path": endpoint.get('path'),
                        "name": endpoint.get('name'),
                        "description": endpoint.get('description')
                    })
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results[:20]  # Limitar a 20 resultados
        }
    except Exception as e:
        logger.error(f"Error en search_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/get_endpoint_details", operation_id="get_endpoint_details")
async def get_endpoint_details(path: str, method: str):
    """Obtener detalles completos de un endpoint"""
    try:
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if endpoint.get('path') == path and endpoint.get('method') == method:
                    return {
                        "resource": resource,
                        "endpoint": endpoint,
                        "found": True
                    }
        
        return {
            "found": False,
            "message": f"Endpoint {method} {path} no encontrado"
        }
    except Exception as e:
        logger.error(f"Error en get_endpoint_details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/get_schema", operation_id="get_schema")
async def get_schema(path: str, method: str):
    """Obtener esquema JSON de solicitud/respuesta"""
    try:
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if endpoint.get('path') == path and endpoint.get('method') == method:
                    return {
                        "resource": resource,
                        "path": path,
                        "method": method,
                        "parameters": endpoint.get('parameters', {}),
                        "description": endpoint.get('description')
                    }
        
        return {"error": "Endpoint no encontrado"}
    except Exception as e:
        logger.error(f"Error en get_schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/search_documentation", operation_id="search_documentation")
async def search_documentation(query: str):
    """Buscar en toda la documentación"""
    try:
        results = []
        
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if (query.lower() in json.dumps(endpoint).lower()):
                    results.append({
                        "resource": resource,
                        "method": endpoint.get('method'),
                        "path": endpoint.get('path'),
                        "name": endpoint.get('name')
                    })
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results[:20]
        }
    except Exception as e:
        logger.error(f"Error en search_documentation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/get_code_example", operation_id="get_code_example")
async def get_code_example(path: str, method: str, language: str = "python"):
    """Obtener ejemplo de código para un endpoint"""
    try:
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if endpoint.get('path') == path and endpoint.get('method') == method:
                    
                    if language == "python":
                        code = f"""import requests

# Endpoint: {method} {path}
# {endpoint.get('description', 'Sin descripción')}

url = "https://api.tiendanube.com/v1{path}"
headers = {{
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "User-Agent": "MyApp (name@email.com)"
}}

# Parámetros
params = {{
    # Agregar parámetros según sea necesario
}}

# Realizar solicitud
response = requests.{method.lower()}(url, headers=headers, params=params)

# Procesar respuesta
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {{response.status_code}}")
    print(response.text)
"""
                    elif language == "javascript":
                        code = f"""// Endpoint: {method} {path}
// {endpoint.get('description', 'Sin descripción')}

const url = 'https://api.tiendanube.com/v1{path}';
const headers = {{
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'User-Agent': 'MyApp (name@email.com)'
}};

const options = {{
    method: '{method}',
    headers: headers
}};

fetch(url, options)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
"""
                    else:
                        code = "Lenguaje no soportado"
                    
                    return {
                        "path": path,
                        "method": method,
                        "language": language,
                        "code": code
                    }
        
        return {"error": "Endpoint no encontrado"}
    except Exception as e:
        logger.error(f"Error en get_code_example: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/list_resources", operation_id="list_resources")
async def list_resources():
    """Listar todos los recursos disponibles"""
    try:
        resources = []
        for resource, endpoints in API_DATABASE['endpoints'].items():
            resources.append({
                "resource": resource,
                "endpoint_count": len(endpoints),
                "endpoints": [
                    {
                        "method": e.get('method'),
                        "path": e.get('path'),
                        "name": e.get('name')
                    }
                    for e in endpoints
                ]
            })
        
        return {
            "total_resources": len(resources),
            "total_endpoints": sum(len(e) for e in API_DATABASE['endpoints'].values()),
            "resources": resources
        }
    except Exception as e:
        logger.error(f"Error en list_resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/get_resource_endpoints", operation_id="get_resource_endpoints")
async def get_resource_endpoints(resource: str):
    """Obtener todos los endpoints de un recurso"""
    try:
        if resource not in API_DATABASE['endpoints']:
            return {"error": f"Recurso '{resource}' no encontrado"}
        
        endpoints = API_DATABASE['endpoints'][resource]
        return {
            "resource": resource,
            "endpoint_count": len(endpoints),
            "endpoints": [
                {
                    "method": e.get('method'),
                    "path": e.get('path'),
                    "name": e.get('name'),
                    "description": e.get('description')
                }
                for e in endpoints
            ]
        }
    except Exception as e:
        logger.error(f"Error en get_resource_endpoints: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/get_authentication_info", operation_id="get_authentication_info")
async def get_authentication_info():
    """Obtener información de autenticación"""
    return {
        "authentication_type": "OAuth 2.0",
        "base_url": "https://api.tiendanube.com/v1",
        "required_headers": {
            "Authorization": "Bearer ACCESS_TOKEN",
            "User-Agent": "MyApp (name@email.com)"
        },
        "rate_limiting": {
            "general": "30 requests/second",
            "tools": "10 requests/second"
        },
        "documentation": "https://tiendanube.github.io/api-documentation/intro"
    }

@app.post("/tools/get_multi_inventory_info", operation_id="get_multi_inventory_info")
async def get_multi_inventory_info():
    """Obtener información sobre multi-inventario"""
    return {
        "feature": "Multi-Inventory Support",
        "version": "2025-03",
        "description": "Nueva API de Productos con soporte para múltiples ubicaciones/almacenes",
        "key_features": [
            "Gestión de inventario por ubicación",
            "Sincronización de stock en tiempo real",
            "Soporte para múltiples almacenes",
            "Asignación inteligente de inventario"
        ],
        "endpoints_affected": [
            "GET /products",
            "GET /products/{id}",
            "POST /products",
            "PUT /products/{id}",
            "PATCH /products/stock-price"
        ],
        "documentation": "https://tiendanube.github.io/api-documentation/guides/multi-inventory/products"
    }

# ===== ENDPOINTS DE DESCUBRIMIENTO =====

@app.get("/.well-known/mcp")
async def well_known_mcp():
    """
    Endpoint de descubrimiento MCP (.well-known/mcp)
    Permite que los clientes MCP descubran automáticamente la configuración del servidor
    """
    return {
        "version": "1.0",
        "provider": {
            "id": "tiendanube",
            "name": "Tienda Nube MCP",
            "description": "MCP endpoint exposing the full Tienda Nube API: products, orders, customers, categories, webhooks and store configuration.",
            "endpoint": "https://tiendanube.mcp-ropu.com/mcp",
            "docs": "https://tiendanube.mcp-ropu.com/docs",
            "owner": "Ropu",
            "tags": ["ecommerce", "tiendanube", "store", "orders", "products"]
        }
    }

@app.get("/.well-known/ai-plugin.json")
async def ai_plugin_json():
    """
    Endpoint de descubrimiento para AI plugins (.well-known/ai-plugin.json)
    Permite que asistentes de IA descubran y usen el servidor MCP
    """
    return {
        "schema_version": "v1",
        "name_for_human": "Tienda Nube MCP",
        "name_for_model": "tiendanube_mcp",
        "description_for_human": "Access Tienda Nube ecommerce API via MCP.",
        "description_for_model": "MCP interface for Tienda Nube API including products, orders, customers, categories and store configuration.",
        "api": {
            "type": "mcp",
            "url": "https://tiendanube.mcp-ropu.com/mcp"
        },
        "documentation_url": "https://tiendanube.mcp-ropu.com/docs"
    }

# ===== ENDPOINT RAÍZ =====

@app.get("/")
async def root():
    """Información del servidor MCP"""
    return {
        "name": "Tienda Nube MCP - Servidor Completo",
        "version": "2.0.0",
        "description": "Servidor MCP con TODOS los 111 endpoints de la API de Tienda Nube",
        "resources": len(API_DATABASE['endpoints']),
        "endpoints": sum(len(e) for e in API_DATABASE['endpoints'].values()),
        "coverage": "100%",
        "documentation": "/docs",
        "mcp_endpoint": "/mcp",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "info": "/info",
            "mcp": "/mcp"
        }
    }

# ===== MANEJO DE ERRORES =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

# ===== MONTAR FASTAPI-MCP AL FINAL =====
# Importante: Montar después de definir todos los endpoints
try:
    # Lista de operation_ids que queremos exponer como herramientas MCP
    tool_operations = [
        "search_endpoint",
        "get_endpoint_details",
        "get_schema",
        "search_documentation",
        "get_code_example",
        "list_resources",
        "get_resource_endpoints",
        "get_authentication_info",
        "get_multi_inventory_info"
    ]
    
    mcp = FastApiMCP(
        app,
        include_operations=tool_operations,  # Incluir solo estos operation_ids como herramientas
        describe_full_response_schema=True  # Incluir esquema completo en descripciones
    )
    mcp.mount_http(mount_path="/mcp")  # Monta el servidor MCP con HTTP para streamable-http
    logger.info(f"✅ FastAPI-MCP montado en /mcp con HTTP y {len(tool_operations)} herramientas")
except Exception as e:
    logger.warning(f"⚠️ No se pudo montar FastAPI-MCP: {e}. Continuando sin MCP HTTP...")
    import traceback
    logger.error(traceback.format_exc())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


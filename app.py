#!/usr/bin/env python3
"""
Servidor HTTP FastAPI para Tienda Nube API MCP
Expone el servidor MCP como una API REST para usar en VPS
"""

import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Importar el servidor MCP
from server_simple import TiendaNubeAPIServer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Tienda Nube API MCP Server",
    description="Servidor MCP para la API de Tienda Nube",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servidor MCP
try:
    mcp_server = TiendaNubeAPIServer()
    logger.info("✓ Servidor MCP inicializado correctamente")
except Exception as e:
    logger.error(f"✗ Error al inicializar servidor MCP: {e}")
    raise


# ============================================================================
# Endpoints de Salud
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Verificar que el servidor está funcionando"""
    return {
        "status": "ok",
        "service": "tiendanube-api-mcp",
        "version": "1.0.0"
    }


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Verificar que el servidor está listo para recibir solicitudes"""
    try:
        # Verificar que la base de datos está cargada
        assert mcp_server.api_database is not None
        assert "endpoints" in mcp_server.api_database
        
        resources = mcp_server.api_database.get("endpoints", {})
        total_endpoints = sum(len(v) for v in resources.values())
        
        return {
            "ready": True,
            "resources": resources,
            "total_endpoints": total_endpoints
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


# ============================================================================
# Endpoints de Herramientas MCP
# ============================================================================

@app.get("/tools", tags=["Tools"])
async def get_tools():
    """Obtener lista de todas las herramientas disponibles"""
    try:
        tools = mcp_server.get_tools_definition()
        return {
            "tools": tools,
            "total": len(tools)
        }
    except Exception as e:
        logger.error(f"Error getting tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/search_endpoint", tags=["Tools"])
async def search_endpoint(
    resource: str = Query(..., description="Recurso: 'products' u 'orders'"),
    method: Optional[str] = Query(None, description="Método HTTP (GET, POST, PUT, PATCH, DELETE)"),
    query: Optional[str] = Query(None, description="Búsqueda por nombre o descripción")
):
    """Buscar endpoints en la API"""
    try:
        result = mcp_server.search_endpoint(resource, method, query)
        return {
            "tool": "search_endpoint",
            "result": json.loads(result)
        }
    except Exception as e:
        logger.error(f"Error in search_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_endpoint_details", tags=["Tools"])
async def get_endpoint_details(
    resource: str = Query(..., description="Recurso: 'products' u 'orders'"),
    path: str = Query(..., description="Ruta del endpoint"),
    method: str = Query("GET", description="Método HTTP")
):
    """Obtener detalles completos de un endpoint"""
    try:
        result = mcp_server.get_endpoint_details(resource, path, method)
        return {
            "tool": "get_endpoint_details",
            "result": json.loads(result)
        }
    except Exception as e:
        logger.error(f"Error in get_endpoint_details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_schema", tags=["Tools"])
async def get_schema(
    resource: str = Query(..., description="Recurso: 'products' u 'orders'"),
    endpoint_type: str = Query("response", description="'request' o 'response'")
):
    """Obtener esquema JSON"""
    try:
        result = mcp_server.get_schema(resource, endpoint_type)
        return {
            "tool": "get_schema",
            "result": json.loads(result)
        }
    except Exception as e:
        logger.error(f"Error in get_schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/search_documentation", tags=["Tools"])
async def search_documentation(
    query: str = Query(..., description="Término de búsqueda")
):
    """Buscar en la documentación"""
    try:
        result = mcp_server.search_documentation(query)
        return {
            "tool": "search_documentation",
            "result": json.loads(result)
        }
    except Exception as e:
        logger.error(f"Error in search_documentation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_code_example", tags=["Tools"])
async def get_code_example(
    resource: str = Query(..., description="Recurso: 'products' u 'orders'"),
    path: str = Query(..., description="Ruta del endpoint"),
    method: str = Query("GET", description="Método HTTP"),
    language: str = Query("python", description="Lenguaje: 'python' o 'javascript'")
):
    """Obtener ejemplo de código"""
    try:
        result = mcp_server.get_code_example(resource, path, method, language)
        return {
            "tool": "get_code_example",
            "result": result
        }
    except Exception as e:
        logger.error(f"Error in get_code_example: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_authentication_info", tags=["Tools"])
async def get_authentication_info():
    """Obtener información de autenticación"""
    try:
        result = mcp_server.get_authentication_info()
        return {
            "tool": "get_authentication_info",
            "result": json.loads(result)
        }
    except Exception as e:
        logger.error(f"Error in get_authentication_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_multi_inventory_info", tags=["Tools"])
async def get_multi_inventory_info():
    """Obtener información sobre multi-inventario"""
    try:
        result = mcp_server.get_multi_inventory_info()
        return {
            "tool": "get_multi_inventory_info",
            "result": json.loads(result)
        }
    except Exception as e:
        logger.error(f"Error in get_multi_inventory_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/list_resources", tags=["Tools"])
async def list_resources():
    """Listar recursos disponibles"""
    try:
        result = mcp_server.list_resources()
        return {
            "tool": "list_resources",
            "result": json.loads(result)
        }
    except Exception as e:
        logger.error(f"Error in list_resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Endpoints de Información
# ============================================================================

@app.get("/info", tags=["Info"])
async def get_info():
    """Obtener información del servidor"""
    try:
        resources = mcp_server.api_database.get("endpoints", {})
        total_endpoints = sum(len(v) for v in resources.values())
        
        return {
            "name": "Tienda Nube API MCP Server",
            "version": "1.0.0",
            "api_version": mcp_server.api_database.get("metadata", {}).get("version", "unknown"),
            "resources": {k: len(v) for k, v in resources.items()},
            "total_endpoints": total_endpoints,
            "tools": len(mcp_server.get_tools_definition()),
            "documentation_url": "https://tiendanube.github.io/api-documentation/"
        }
    except Exception as e:
        logger.error(f"Error in get_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/endpoints", tags=["Info"])
async def get_all_endpoints(resource: Optional[str] = Query(None)):
    """Obtener lista de todos los endpoints"""
    try:
        endpoints_data = mcp_server.api_database.get("endpoints", {})
        
        if resource:
            if resource not in endpoints_data:
                raise HTTPException(status_code=404, detail=f"Recurso '{resource}' no encontrado")
            endpoints_data = {resource: endpoints_data[resource]}
        
        result = {}
        for res_name, endpoints in endpoints_data.items():
            result[res_name] = [
                {
                    "method": ep.get("method"),
                    "path": ep.get("path"),
                    "name": ep.get("name"),
                    "description": ep.get("description")
                }
                for ep in endpoints
            ]
        
        return {
            "endpoints": result,
            "total": sum(len(v) for v in result.values())
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_all_endpoints: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Root
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "Tienda Nube API MCP Server",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "ready": "/ready",
        "info": "/info"
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejador general de excepciones"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# ============================================================================
# Startup/Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Evento de inicio"""
    logger.info("=" * 60)
    logger.info("Tienda Nube API MCP Server iniciado")
    logger.info("=" * 60)
    logger.info(f"Documentación disponible en: http://localhost:8000/docs")
    logger.info(f"Health check: http://localhost:8000/health")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre"""
    logger.info("Tienda Nube API MCP Server detenido")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Configuración de Uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )

#!/usr/bin/env python3
"""
Tienda Nube API MCP Server
Servidor Model Context Protocol para la API de Tienda Nube
Permite a Cursor codear usando la API de Tienda Nube
"""

import json
import sys
from pathlib import Path
from typing import Any

# Importar la librería de MCP
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent, ToolResult
except ImportError:
    print("Error: Instala mcp con: pip install mcp", file=sys.stderr)
    sys.exit(1)


class TiendaNubeAPIServer:
    """Servidor MCP para la API de Tienda Nube"""

    def __init__(self):
        self.server = Server("tiendanube-api")
        self.api_database = self._load_api_database()
        self._register_tools()

    def _load_api_database(self) -> dict:
        """Cargar la base de datos de la API"""
        db_path = Path(__file__).parent / "api_database.json"
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _register_tools(self):
        """Registrar todas las herramientas disponibles"""
        
        @self.server.call_tool()
        def search_endpoint(resource: str, method: str = None, query: str = None) -> str:
            """
            Buscar endpoints en la API de Tienda Nube
            
            Args:
                resource: Recurso a buscar ('products' o 'orders')
                method: Método HTTP (GET, POST, PUT, PATCH, DELETE) - opcional
                query: Búsqueda por nombre o descripción - opcional
            
            Returns:
                Lista de endpoints que coinciden con la búsqueda
            """
            endpoints = self.api_database.get("endpoints", {}).get(resource, [])
            
            if not endpoints:
                return f"No se encontraron endpoints para el recurso '{resource}'"
            
            results = []
            for endpoint in endpoints:
                # Filtrar por método si se especifica
                if method and endpoint.get("method") != method.upper():
                    continue
                
                # Filtrar por query si se especifica
                if query:
                    query_lower = query.lower()
                    if not (query_lower in endpoint.get("name", "").lower() or
                           query_lower in endpoint.get("description", "").lower() or
                           query_lower in endpoint.get("path", "").lower()):
                        continue
                
                results.append({
                    "method": endpoint.get("method"),
                    "path": endpoint.get("path"),
                    "name": endpoint.get("name"),
                    "description": endpoint.get("description")
                })
            
            if not results:
                return f"No se encontraron endpoints que coincidan con los criterios"
            
            return json.dumps(results, indent=2, ensure_ascii=False)

        @self.server.call_tool()
        def get_endpoint_details(resource: str, path: str, method: str = "GET") -> str:
            """
            Obtener detalles completos de un endpoint
            
            Args:
                resource: Recurso ('products' o 'orders')
                path: Ruta del endpoint (ej: '/products', '/orders/{id}')
                method: Método HTTP (GET, POST, PUT, PATCH, DELETE)
            
            Returns:
                Detalles completos del endpoint incluyendo parámetros, esquema y ejemplos
            """
            endpoints = self.api_database.get("endpoints", {}).get(resource, [])
            
            for endpoint in endpoints:
                if endpoint.get("path") == path and endpoint.get("method") == method.upper():
                    return json.dumps(endpoint, indent=2, ensure_ascii=False)
            
            return f"Endpoint no encontrado: {method} {path}"

        @self.server.call_tool()
        def get_schema(resource: str, endpoint_type: str = "response") -> str:
            """
            Obtener esquema JSON de solicitud o respuesta
            
            Args:
                resource: Recurso ('products' o 'orders')
                endpoint_type: 'request' para esquema de solicitud, 'response' para respuesta
            
            Returns:
                Esquema JSON en formato legible
            """
            endpoints = self.api_database.get("endpoints", {}).get(resource, [])
            
            schemas = []
            for endpoint in endpoints:
                if endpoint_type == "request" and "request_schema" in endpoint:
                    schemas.append({
                        "method": endpoint.get("method"),
                        "path": endpoint.get("path"),
                        "schema": endpoint.get("request_schema")
                    })
                elif endpoint_type == "response" and "response_schema" in endpoint:
                    schemas.append({
                        "method": endpoint.get("method"),
                        "path": endpoint.get("path"),
                        "schema": endpoint.get("response_schema")
                    })
            
            if not schemas:
                return f"No se encontraron esquemas de {endpoint_type} para {resource}"
            
            return json.dumps(schemas, indent=2, ensure_ascii=False)

        @self.server.call_tool()
        def search_documentation(query: str) -> str:
            """
            Buscar en la documentación por palabras clave
            
            Args:
                query: Término de búsqueda
            
            Returns:
                Resultados relevantes de la documentación
            """
            query_lower = query.lower()
            results = []
            
            # Buscar en endpoints
            for resource_name, endpoints in self.api_database.get("endpoints", {}).items():
                for endpoint in endpoints:
                    if (query_lower in endpoint.get("name", "").lower() or
                        query_lower in endpoint.get("description", "").lower() or
                        query_lower in endpoint.get("path", "").lower()):
                        results.append({
                            "type": "endpoint",
                            "resource": resource_name,
                            "method": endpoint.get("method"),
                            "path": endpoint.get("path"),
                            "name": endpoint.get("name"),
                            "description": endpoint.get("description")
                        })
            
            # Buscar en notas importantes
            for note_key, note_data in self.api_database.get("important_notes", {}).items():
                if (query_lower in note_key.lower() or
                    query_lower in str(note_data).lower()):
                    results.append({
                        "type": "note",
                        "key": note_key,
                        "data": note_data
                    })
            
            if not results:
                return f"No se encontraron resultados para: {query}"
            
            return json.dumps(results, indent=2, ensure_ascii=False)

        @self.server.call_tool()
        def get_code_example(resource: str, path: str, method: str = "GET", language: str = "python") -> str:
            """
            Obtener ejemplo de código para un endpoint
            
            Args:
                resource: Recurso ('products' u 'orders')
                path: Ruta del endpoint
                method: Método HTTP
                language: Lenguaje de programación ('python' o 'javascript')
            
            Returns:
                Ejemplo de código en el lenguaje especificado
            """
            endpoints = self.api_database.get("endpoints", {}).get(resource, [])
            
            for endpoint in endpoints:
                if endpoint.get("path") == path and endpoint.get("method") == method.upper():
                    examples = endpoint.get("code_examples", {})
                    if language in examples:
                        return examples[language]
                    else:
                        available = list(examples.keys())
                        return f"Ejemplo no disponible en {language}. Disponibles: {', '.join(available)}"
            
            return f"Endpoint no encontrado: {method} {path}"

        @self.server.call_tool()
        def get_authentication_info() -> str:
            """
            Obtener información sobre autenticación en la API
            
            Returns:
                Detalles de autenticación y scopes disponibles
            """
            auth_info = self.api_database.get("important_notes", {}).get("authentication", {})
            return json.dumps(auth_info, indent=2, ensure_ascii=False)

        @self.server.call_tool()
        def get_multi_inventory_info() -> str:
            """
            Obtener información sobre la nueva API de Productos con multi-inventario
            
            Returns:
                Detalles sobre cambios y migración a multi-inventario
            """
            multi_inv = self.api_database.get("important_notes", {}).get("multi_inventory", {})
            return json.dumps(multi_inv, indent=2, ensure_ascii=False)

        @self.server.call_tool()
        def list_resources() -> str:
            """
            Listar todos los recursos disponibles en la API
            
            Returns:
                Lista de recursos y cantidad de endpoints
            """
            resources = {}
            for resource_name, endpoints in self.api_database.get("endpoints", {}).items():
                resources[resource_name] = len(endpoints)
            
            return json.dumps({
                "resources": resources,
                "total_endpoints": sum(resources.values())
            }, indent=2, ensure_ascii=False)

    def run(self):
        """Ejecutar el servidor MCP"""
        self.server.run()


if __name__ == "__main__":
    server = TiendaNubeAPIServer()
    server.run()

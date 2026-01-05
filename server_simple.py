#!/usr/bin/env python3
"""
Tienda Nube API MCP Server - Versión Simplificada
Servidor Model Context Protocol para la API de Tienda Nube
Compatible con Cursor y otros clientes MCP
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


class TiendaNubeAPIServer:
    """Servidor MCP para la API de Tienda Nube"""

    def __init__(self):
        self.api_database = self._load_api_database()
        self.tools = self._get_tools()

    def _load_api_database(self) -> dict:
        """Cargar la base de datos de la API"""
        db_path = Path(__file__).parent / "api_database.json"
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_tools(self) -> List[Dict[str, Any]]:
        """Definir todas las herramientas disponibles"""
        return [
            {
                "name": "search_endpoint",
                "description": "Buscar endpoints en la API de Tienda Nube por recurso, método o nombre",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Recurso a buscar: 'products' u 'orders'",
                            "enum": ["products", "orders"]
                        },
                        "method": {
                            "type": "string",
                            "description": "Método HTTP (GET, POST, PUT, PATCH, DELETE) - opcional",
                            "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                        },
                        "query": {
                            "type": "string",
                            "description": "Búsqueda por nombre o descripción - opcional"
                        }
                    },
                    "required": ["resource"]
                }
            },
            {
                "name": "get_endpoint_details",
                "description": "Obtener detalles completos de un endpoint incluyendo parámetros, esquema y ejemplos",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Recurso: 'products' u 'orders'",
                            "enum": ["products", "orders"]
                        },
                        "path": {
                            "type": "string",
                            "description": "Ruta del endpoint (ej: '/products', '/orders/{id}')"
                        },
                        "method": {
                            "type": "string",
                            "description": "Método HTTP",
                            "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                            "default": "GET"
                        }
                    },
                    "required": ["resource", "path"]
                }
            },
            {
                "name": "get_schema",
                "description": "Obtener esquema JSON de solicitud o respuesta para un recurso",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Recurso: 'products' u 'orders'",
                            "enum": ["products", "orders"]
                        },
                        "endpoint_type": {
                            "type": "string",
                            "description": "'request' para esquema de solicitud, 'response' para respuesta",
                            "enum": ["request", "response"],
                            "default": "response"
                        }
                    },
                    "required": ["resource"]
                }
            },
            {
                "name": "search_documentation",
                "description": "Buscar en la documentación por palabras clave",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Término de búsqueda"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_code_example",
                "description": "Obtener ejemplo de código para un endpoint",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Recurso: 'products' u 'orders'",
                            "enum": ["products", "orders"]
                        },
                        "path": {
                            "type": "string",
                            "description": "Ruta del endpoint"
                        },
                        "method": {
                            "type": "string",
                            "description": "Método HTTP",
                            "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                            "default": "GET"
                        },
                        "language": {
                            "type": "string",
                            "description": "Lenguaje de programación",
                            "enum": ["python", "javascript"],
                            "default": "python"
                        }
                    },
                    "required": ["resource", "path"]
                }
            },
            {
                "name": "get_authentication_info",
                "description": "Obtener información sobre autenticación en la API",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_multi_inventory_info",
                "description": "Obtener información sobre la nueva API de Productos con multi-inventario",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "list_resources",
                "description": "Listar todos los recursos disponibles en la API",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

    def search_endpoint(self, resource: str, method: str = None, query: str = None) -> str:
        """Buscar endpoints"""
        endpoints = self.api_database.get("endpoints", {}).get(resource, [])
        
        if not endpoints:
            return f"No se encontraron endpoints para el recurso '{resource}'"
        
        results = []
        for endpoint in endpoints:
            if method and endpoint.get("method") != method.upper():
                continue
            
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

    def get_endpoint_details(self, resource: str, path: str, method: str = "GET") -> str:
        """Obtener detalles de un endpoint"""
        endpoints = self.api_database.get("endpoints", {}).get(resource, [])
        
        for endpoint in endpoints:
            if endpoint.get("path") == path and endpoint.get("method") == method.upper():
                return json.dumps(endpoint, indent=2, ensure_ascii=False)
        
        return f"Endpoint no encontrado: {method} {path}"

    def get_schema(self, resource: str, endpoint_type: str = "response") -> str:
        """Obtener esquema"""
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

    def search_documentation(self, query: str) -> str:
        """Buscar en documentación"""
        query_lower = query.lower()
        results = []
        
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

    def get_code_example(self, resource: str, path: str, method: str = "GET", language: str = "python") -> str:
        """Obtener ejemplo de código"""
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

    def get_authentication_info(self) -> str:
        """Obtener info de autenticación"""
        auth_info = self.api_database.get("important_notes", {}).get("authentication", {})
        return json.dumps(auth_info, indent=2, ensure_ascii=False)

    def get_multi_inventory_info(self) -> str:
        """Obtener info de multi-inventario"""
        multi_inv = self.api_database.get("important_notes", {}).get("multi_inventory", {})
        return json.dumps(multi_inv, indent=2, ensure_ascii=False)

    def list_resources(self) -> str:
        """Listar recursos"""
        resources = {}
        for resource_name, endpoints in self.api_database.get("endpoints", {}).items():
            resources[resource_name] = len(endpoints)
        
        return json.dumps({
            "resources": resources,
            "total_endpoints": sum(resources.values())
        }, indent=2, ensure_ascii=False)

    def process_tool_call(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Procesar llamada a herramienta"""
        if tool_name == "search_endpoint":
            return self.search_endpoint(**tool_input)
        elif tool_name == "get_endpoint_details":
            return self.get_endpoint_details(**tool_input)
        elif tool_name == "get_schema":
            return self.get_schema(**tool_input)
        elif tool_name == "search_documentation":
            return self.search_documentation(**tool_input)
        elif tool_name == "get_code_example":
            return self.get_code_example(**tool_input)
        elif tool_name == "get_authentication_info":
            return self.get_authentication_info()
        elif tool_name == "get_multi_inventory_info":
            return self.get_multi_inventory_info()
        elif tool_name == "list_resources":
            return self.list_resources()
        else:
            return f"Herramienta desconocida: {tool_name}"

    def get_tools_definition(self) -> List[Dict[str, Any]]:
        """Obtener definición de herramientas"""
        return self.tools


if __name__ == "__main__":
    # Para testing
    server = TiendaNubeAPIServer()
    
    # Ejemplo de uso
    print("=== Tienda Nube API MCP Server ===\n")
    print("Herramientas disponibles:")
    for tool in server.tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\n=== Ejemplos de uso ===\n")
    
    # Buscar endpoints
    print("1. Buscar endpoints de productos:")
    result = server.search_endpoint("products")
    print(result[:500] + "...\n")
    
    # Obtener detalles
    print("2. Obtener detalles de GET /products:")
    result = server.get_endpoint_details("products", "/products")
    print(result[:500] + "...\n")
    
    # Listar recursos
    print("3. Listar recursos disponibles:")
    print(server.list_resources())

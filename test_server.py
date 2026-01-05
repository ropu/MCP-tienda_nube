#!/usr/bin/env python3
"""
Script de pruebas para el servidor MCP de Tienda Nube
Valida que todas las herramientas funcionen correctamente
"""

import json
import sys
from pathlib import Path

# Importar el servidor
sys.path.insert(0, str(Path(__file__).parent))
from server_simple import TiendaNubeAPIServer


def print_section(title):
    """Imprimir encabezado de sección"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_server():
    """Ejecutar todas las pruebas"""
    
    print_section("Iniciando Pruebas del Servidor MCP de Tienda Nube")
    
    try:
        server = TiendaNubeAPIServer()
        print("✓ Servidor inicializado correctamente")
    except Exception as e:
        print(f"✗ Error al inicializar servidor: {e}")
        return False
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Verificar que la base de datos se cargó
    print_section("Test 1: Cargar Base de Datos")
    try:
        assert server.api_database is not None
        assert "endpoints" in server.api_database
        assert "products" in server.api_database["endpoints"]
        assert "orders" in server.api_database["endpoints"]
        print(f"✓ Base de datos cargada correctamente")
        print(f"  - Recursos: {list(server.api_database['endpoints'].keys())}")
        print(f"  - Total endpoints: {sum(len(v) for v in server.api_database['endpoints'].values())}")
        tests_passed += 1
    except AssertionError as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 2: search_endpoint - Productos
    print_section("Test 2: search_endpoint - Productos")
    try:
        result = server.search_endpoint("products")
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        assert "method" in data[0]
        assert "path" in data[0]
        print(f"✓ search_endpoint funciona correctamente")
        print(f"  - Encontrados {len(data)} endpoints de productos")
        print(f"  - Ejemplo: {data[0]['method']} {data[0]['path']}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 3: search_endpoint - Órdenes
    print_section("Test 3: search_endpoint - Órdenes")
    try:
        result = server.search_endpoint("orders")
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ search_endpoint funciona para órdenes")
        print(f"  - Encontrados {len(data)} endpoints de órdenes")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 4: search_endpoint - Filtrar por método
    print_section("Test 4: search_endpoint - Filtrar por método POST")
    try:
        result = server.search_endpoint("products", method="POST")
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        assert all(item["method"] == "POST" for item in data)
        print(f"✓ Filtro por método funciona")
        print(f"  - Encontrados {len(data)} endpoints POST")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 5: get_endpoint_details
    print_section("Test 5: get_endpoint_details - GET /products")
    try:
        result = server.get_endpoint_details("products", "/products", "GET")
        data = json.loads(result)
        assert data["method"] == "GET"
        assert data["path"] == "/products"
        assert "parameters" in data
        assert "response_schema" in data
        print(f"✓ get_endpoint_details funciona correctamente")
        print(f"  - Endpoint: {data['method']} {data['path']}")
        print(f"  - Parámetros: {len(data['parameters'])}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 6: get_endpoint_details - POST /products
    print_section("Test 6: get_endpoint_details - POST /products")
    try:
        result = server.get_endpoint_details("products", "/products", "POST")
        data = json.loads(result)
        assert data["method"] == "POST"
        assert "request_schema" in data
        print(f"✓ POST /products tiene esquema de solicitud")
        print(f"  - Campos requeridos: {data['request_schema'].get('required', [])}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 7: get_schema - Productos
    print_section("Test 7: get_schema - Respuesta de Productos")
    try:
        result = server.get_schema("products", "response")
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ get_schema funciona para respuestas")
        print(f"  - Esquemas encontrados: {len(data)}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 8: get_schema - Solicitudes
    print_section("Test 8: get_schema - Solicitud de Productos")
    try:
        result = server.get_schema("products", "request")
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ get_schema funciona para solicitudes")
        print(f"  - Esquemas de solicitud encontrados: {len(data)}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 9: search_documentation
    print_section("Test 9: search_documentation - 'multi-inventario'")
    try:
        result = server.search_documentation("multi-inventario")
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ search_documentation funciona")
        print(f"  - Resultados encontrados: {len(data)}")
        for item in data[:2]:
            print(f"    - {item.get('type')}: {item.get('name', item.get('key', 'N/A'))}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 10: search_documentation - 'stock'
    print_section("Test 10: search_documentation - 'stock'")
    try:
        result = server.search_documentation("stock")
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ Búsqueda por 'stock' funciona")
        print(f"  - Resultados encontrados: {len(data)}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 11: get_code_example - Python
    print_section("Test 11: get_code_example - Python")
    try:
        result = server.get_code_example("products", "/products", "GET", "python")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "requests" in result or "import" in result
        print(f"✓ get_code_example funciona para Python")
        print(f"  - Longitud del ejemplo: {len(result)} caracteres")
        print(f"  - Primeras líneas:")
        for line in result.split('\n')[:3]:
            print(f"    {line}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 12: get_code_example - JavaScript
    print_section("Test 12: get_code_example - JavaScript")
    try:
        result = server.get_code_example("products", "/products", "GET", "javascript")
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"✓ get_code_example funciona para JavaScript")
        print(f"  - Longitud del ejemplo: {len(result)} caracteres")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 13: get_authentication_info
    print_section("Test 13: get_authentication_info")
    try:
        result = server.get_authentication_info()
        data = json.loads(result)
        assert "type" in data
        assert data["type"] == "Bearer Token"
        assert "scopes" in data
        print(f"✓ get_authentication_info funciona")
        print(f"  - Tipo: {data['type']}")
        print(f"  - Scopes: {', '.join(data['scopes'])}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 14: get_multi_inventory_info
    print_section("Test 14: get_multi_inventory_info")
    try:
        result = server.get_multi_inventory_info()
        data = json.loads(result)
        assert "title" in data
        assert "key_changes" in data
        assert isinstance(data["key_changes"], list)
        print(f"✓ get_multi_inventory_info funciona")
        print(f"  - Título: {data['title']}")
        print(f"  - Cambios clave: {len(data['key_changes'])}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 15: list_resources
    print_section("Test 15: list_resources")
    try:
        result = server.list_resources()
        data = json.loads(result)
        assert "resources" in data
        assert "total_endpoints" in data
        assert data["total_endpoints"] > 0
        print(f"✓ list_resources funciona")
        print(f"  - Recursos: {data['resources']}")
        print(f"  - Total endpoints: {data['total_endpoints']}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 16: process_tool_call
    print_section("Test 16: process_tool_call")
    try:
        result = server.process_tool_call("list_resources", {})
        data = json.loads(result)
        assert "resources" in data
        print(f"✓ process_tool_call funciona")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Test 17: get_tools_definition
    print_section("Test 17: get_tools_definition")
    try:
        tools = server.get_tools_definition()
        assert isinstance(tools, list)
        assert len(tools) > 0
        assert all("name" in tool for tool in tools)
        assert all("description" in tool for tool in tools)
        assert all("inputSchema" in tool for tool in tools)
        print(f"✓ get_tools_definition funciona")
        print(f"  - Total herramientas: {len(tools)}")
        for tool in tools:
            print(f"    - {tool['name']}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Error: {e}")
        tests_failed += 1
    
    # Resumen
    print_section("RESUMEN DE PRUEBAS")
    total_tests = tests_passed + tests_failed
    print(f"Total de pruebas: {total_tests}")
    print(f"✓ Pasadas: {tests_passed}")
    print(f"✗ Fallidas: {tests_failed}")
    
    if tests_failed == 0:
        print("\n🎉 ¡Todas las pruebas pasaron correctamente!")
        return True
    else:
        print(f"\n⚠️  {tests_failed} prueba(s) fallaron")
        return False


if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)

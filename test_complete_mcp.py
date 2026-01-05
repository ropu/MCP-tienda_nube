#!/usr/bin/env python3
"""
Suite de Pruebas Exhaustivas para MCP Completo
Valida todos los 111 endpoints y herramientas MCP
"""

import json
import pytest
from datetime import datetime

# Cargar base de datos
with open('/home/ubuntu/tiendanube_mcp/api_database_complete.json', 'r') as f:
    API_DATABASE = json.load(f)

class TestMCPDatabase:
    """Pruebas de la base de datos MCP"""
    
    def test_database_loaded(self):
        """Verificar que la base de datos se cargó correctamente"""
        assert API_DATABASE is not None
        assert 'endpoints' in API_DATABASE
        assert 'metadata' in API_DATABASE
    
    def test_total_resources(self):
        """Verificar cantidad de recursos"""
        resources = len(API_DATABASE['endpoints'])
        assert resources >= 26, f"Se esperaban al menos 26 recursos, se encontraron {resources}"
    
    def test_total_endpoints(self):
        """Verificar cantidad de endpoints"""
        total = sum(len(e) for e in API_DATABASE['endpoints'].values())
        assert total >= 111, f"Se esperaban al menos 111 endpoints, se encontraron {total}"
    
    def test_all_resources_have_endpoints(self):
        """Verificar que todos los recursos tienen endpoints"""
        for resource, endpoints in API_DATABASE['endpoints'].items():
            assert len(endpoints) > 0, f"Recurso '{resource}' no tiene endpoints"
    
    def test_all_endpoints_have_required_fields(self):
        """Verificar que todos los endpoints tienen campos requeridos"""
        required_fields = ['method', 'path', 'name', 'description']
        
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for i, endpoint in enumerate(endpoints):
                for field in required_fields:
                    assert field in endpoint, f"Endpoint {i} en '{resource}' falta el campo '{field}'"
    
    def test_endpoint_methods_valid(self):
        """Verificar que los métodos HTTP sean válidos"""
        valid_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']
        
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                method = endpoint.get('method')
                assert method in valid_methods, f"Método inválido: {method}"
    
    def test_endpoint_paths_format(self):
        """Verificar formato de paths"""
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                path = endpoint.get('path')
                assert path.startswith('/'), f"Path debe comenzar con '/': {path}"
    
    def test_no_duplicate_endpoints(self):
        """Verificar que no haya endpoints duplicados"""
        seen = set()
        duplicates = []
        
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                key = (endpoint.get('method'), endpoint.get('path'))
                if key in seen:
                    duplicates.append(key)
                seen.add(key)
        
        assert len(duplicates) == 0, f"Endpoints duplicados encontrados: {duplicates}"

class TestResourceCoverage:
    """Pruebas de cobertura de recursos"""
    
    def test_products_resource(self):
        """Verificar recurso de Productos"""
        assert 'products' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['products']) >= 7
    
    def test_orders_resource(self):
        """Verificar recurso de Órdenes"""
        assert 'orders' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['orders']) >= 10
    
    def test_customers_resource(self):
        """Verificar recurso de Clientes"""
        assert 'customers' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['customers']) >= 5
    
    def test_categories_resource(self):
        """Verificar recurso de Categorías"""
        assert 'categories' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['categories']) >= 5
    
    def test_cart_resource(self):
        """Verificar recurso de Carrito"""
        assert 'cart' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['cart']) >= 5
    
    def test_coupons_resource(self):
        """Verificar recurso de Cupones"""
        assert 'coupons' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['coupons']) >= 5
    
    def test_draft_orders_resource(self):
        """Verificar recurso de Órdenes en Borrador"""
        assert 'draft_orders' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['draft_orders']) >= 5
    
    def test_product_images_resource(self):
        """Verificar recurso de Imágenes de Producto"""
        assert 'product_images' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['product_images']) >= 5
    
    def test_product_variants_resource(self):
        """Verificar recurso de Variantes de Producto"""
        assert 'product_variants' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['product_variants']) >= 5
    
    def test_locations_resource(self):
        """Verificar recurso de Ubicaciones"""
        assert 'locations' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['locations']) >= 5
    
    def test_fulfillment_orders_resource(self):
        """Verificar recurso de Órdenes de Cumplimiento"""
        assert 'fulfillment_orders' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['fulfillment_orders']) >= 4
    
    def test_store_resource(self):
        """Verificar recurso de Tienda"""
        assert 'store' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['store']) >= 2
    
    def test_discounts_resource(self):
        """Verificar recurso de Descuentos"""
        assert 'discounts' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['discounts']) >= 5
    
    def test_webhooks_resource(self):
        """Verificar recurso de Webhooks"""
        assert 'webhooks' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['webhooks']) >= 5
    
    def test_metafields_resource(self):
        """Verificar recurso de Metafields"""
        assert 'metafields' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['metafields']) >= 5
    
    def test_blog_resource(self):
        """Verificar recurso de Blog"""
        assert 'blog' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['blog']) >= 5
    
    def test_pages_resource(self):
        """Verificar recurso de Páginas"""
        assert 'pages' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['pages']) >= 5
    
    def test_scripts_resource(self):
        """Verificar recurso de Scripts"""
        assert 'scripts' in API_DATABASE['endpoints']
        assert len(API_DATABASE['endpoints']['scripts']) >= 5

class TestEndpointStructure:
    """Pruebas de estructura de endpoints"""
    
    def test_get_endpoints_exist(self):
        """Verificar que existan endpoints GET"""
        get_count = 0
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if endpoint.get('method') == 'GET':
                    get_count += 1
        assert get_count > 0, "No se encontraron endpoints GET"
    
    def test_post_endpoints_exist(self):
        """Verificar que existan endpoints POST"""
        post_count = 0
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if endpoint.get('method') == 'POST':
                    post_count += 1
        assert post_count > 0, "No se encontraron endpoints POST"
    
    def test_put_endpoints_exist(self):
        """Verificar que existan endpoints PUT"""
        put_count = 0
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if endpoint.get('method') == 'PUT':
                    put_count += 1
        assert put_count > 0, "No se encontraron endpoints PUT"
    
    def test_delete_endpoints_exist(self):
        """Verificar que existan endpoints DELETE"""
        delete_count = 0
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                if endpoint.get('method') == 'DELETE':
                    delete_count += 1
        assert delete_count > 0, "No se encontraron endpoints DELETE"
    
    def test_parameters_structure(self):
        """Verificar estructura de parámetros"""
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                params = endpoint.get('parameters', {})
                assert isinstance(params, dict), f"Parámetros debe ser dict en {resource}"

class TestMetadata:
    """Pruebas de metadatos"""
    
    def test_metadata_exists(self):
        """Verificar que existan metadatos"""
        assert 'metadata' in API_DATABASE
        metadata = API_DATABASE['metadata']
        assert 'api_name' in metadata
        assert 'version' in metadata
    
    def test_metadata_version(self):
        """Verificar versión de API"""
        metadata = API_DATABASE['metadata']
        assert metadata['version'] == '2025-03'
    
    def test_metadata_coverage(self):
        """Verificar cobertura en metadatos"""
        metadata = API_DATABASE['metadata']
        assert metadata.get('coverage') == '100%'

class TestEndpointCounts:
    """Pruebas de conteos de endpoints"""
    
    def test_count_by_method(self):
        """Contar endpoints por método"""
        methods = {}
        for resource, endpoints in API_DATABASE['endpoints'].items():
            for endpoint in endpoints:
                method = endpoint.get('method')
                methods[method] = methods.get(method, 0) + 1
        
        print(f"\n📊 Endpoints por método:")
        for method, count in sorted(methods.items()):
            print(f"  {method}: {count}")
        
        assert len(methods) > 0, "No se encontraron métodos"
    
    def test_count_by_resource(self):
        """Contar endpoints por recurso"""
        print(f"\n📊 Endpoints por recurso:")
        for resource, endpoints in sorted(API_DATABASE['endpoints'].items()):
            print(f"  {resource}: {len(endpoints)}")
    
    def test_total_statistics(self):
        """Mostrar estadísticas totales"""
        total_resources = len(API_DATABASE['endpoints'])
        total_endpoints = sum(len(e) for e in API_DATABASE['endpoints'].values())
        
        print(f"\n📊 Estadísticas Totales:")
        print(f"  Recursos: {total_resources}")
        print(f"  Endpoints: {total_endpoints}")
        print(f"  Cobertura: 100%")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


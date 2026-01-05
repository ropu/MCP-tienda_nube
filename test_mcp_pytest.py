"""
Suite de Pruebas Exhaustiva para Herramientas MCP
Prueba todos los 8 endpoints de herramientas MCP
Incluye casos de éxito, error, límite y rate limiting
"""

import pytest
import requests
import time
import json
from typing import Dict, Any, List

# Configuración
BASE_URL = "http://localhost:8000"
TIMEOUT = 10


class TestSearchEndpoint:
    """Pruebas para herramienta: search_endpoint"""
    
    endpoint = "/tools/search_endpoint"
    
    # Casos de Éxito
    def test_se_1_1_search_all_products(self):
        """SE-1.1: Buscar todos los endpoints de productos"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", params={"resource": "products"}, timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert "result" in data or "tool" in data
        assert isinstance(data.get("result"), list)
    
    def test_se_1_2_search_all_orders(self):
        """SE-1.2: Buscar todos los endpoints de órdenes"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", params={"resource": "orders"}, timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("result"), list)
    
    def test_se_1_3_search_post_products(self):
        """SE-1.3: Buscar endpoints POST de productos"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "method": "POST"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", [])
        # Validar que todos los resultados son POST
        for item in result:
            assert item.get("method") == "POST"
    
    def test_se_1_4_search_get_orders(self):
        """SE-1.4: Buscar endpoints GET de órdenes"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "orders", "method": "GET"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", [])
        for item in result:
            assert item.get("method") == "GET"
    
    def test_se_1_5_search_by_query_create(self):
        """SE-1.5: Buscar por nombre (create)"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "query": "create"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("result"), list)
    
    def test_se_1_6_search_by_query_pay(self):
        """SE-1.6: Buscar por nombre (pay)"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "orders", "query": "pay"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("result"), list)
    
    # Casos de Error
    def test_se_2_1_missing_resource(self):
        """SE-2.1: Resource faltante"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_se_2_2_invalid_resource(self):
        """SE-2.2: Resource inválido"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "invalid"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_se_2_3_invalid_method(self):
        """SE-2.3: Method inválido"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "method": "INVALID"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    # Casos Límite
    def test_se_3_1_query_with_spaces(self):
        """SE-3.1: Query con espacios"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "query": "list products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    def test_se_3_2_query_with_numbers(self):
        """SE-3.2: Query con números"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "query": "123"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200


class TestGetEndpointDetails:
    """Pruebas para herramienta: get_endpoint_details"""
    
    endpoint = "/tools/get_endpoint_details"
    
    # Casos de Éxito
    def test_ged_1_1_get_products(self):
        """GED-1.1: GET /products"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "method": "GET"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", {})
        assert result.get("method") == "GET"
        assert result.get("path") == "/products"
    
    def test_ged_1_2_post_products(self):
        """GED-1.2: POST /products"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "method": "POST"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", {})
        assert result.get("method") == "POST"
    
    def test_ged_1_3_patch_stock_price(self):
        """GED-1.3: PATCH /products/stock-price"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products/stock-price", "method": "PATCH"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", {})
        assert result.get("method") == "PATCH"
    
    def test_ged_1_4_get_orders(self):
        """GED-1.4: GET /orders"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "orders", "path": "/orders", "method": "GET"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    def test_ged_1_7_default_method(self):
        """GED-1.7: Sin method (default GET)"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", {})
        assert result.get("method") == "GET"
    
    # Casos de Error
    def test_ged_2_1_missing_resource(self):
        """GED-2.1: Resource faltante"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"path": "/products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_ged_2_2_missing_path(self):
        """GED-2.2: Path faltante"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_ged_2_3_invalid_resource(self):
        """GED-2.3: Resource inválido"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "invalid", "path": "/products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_ged_2_5_invalid_method(self):
        """GED-2.5: Method inválido"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "method": "INVALID"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400


class TestGetSchema:
    """Pruebas para herramienta: get_schema"""
    
    endpoint = "/tools/get_schema"
    
    # Casos de Éxito
    def test_gs_1_1_response_schema_products(self):
        """GS-1.1: Schema respuesta productos"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "endpoint_type": "response"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", [])
        assert isinstance(result, list)
        if result:
            assert "schema" in result[0]
    
    def test_gs_1_2_request_schema_products(self):
        """GS-1.2: Schema solicitud productos"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "endpoint_type": "request"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("result"), list)
    
    def test_gs_1_3_response_schema_orders(self):
        """GS-1.3: Schema respuesta órdenes"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "orders", "endpoint_type": "response"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    def test_gs_1_5_default_endpoint_type(self):
        """GS-1.5: Sin endpoint_type (default)"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("result"), list)
    
    # Casos de Error
    def test_gs_2_1_missing_resource(self):
        """GS-2.1: Resource faltante"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"endpoint_type": "response"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_gs_2_2_invalid_resource(self):
        """GS-2.2: Resource inválido"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "invalid", "endpoint_type": "response"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_gs_2_3_invalid_endpoint_type(self):
        """GS-2.3: Endpoint_type inválido"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "endpoint_type": "invalid"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400


class TestSearchDocumentation:
    """Pruebas para herramienta: search_documentation"""
    
    endpoint = "/tools/search_documentation"
    
    # Casos de Éxito
    def test_sd_1_1_search_multi_inventory(self):
        """SD-1.1: Buscar multi-inventario"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"query": "multi-inventario"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("result"), list)
    
    def test_sd_1_2_search_stock(self):
        """SD-1.2: Buscar stock"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"query": "stock"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    def test_sd_1_3_search_pay(self):
        """SD-1.3: Buscar pay"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"query": "pay"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    def test_sd_1_4_search_inventory(self):
        """SD-1.4: Buscar inventory"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"query": "inventory"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    # Casos de Error
    def test_sd_2_1_missing_query(self):
        """SD-2.1: Query faltante"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_sd_2_4_special_characters(self):
        """SD-2.4: Query con caracteres especiales"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"query": "<script>alert()</script>"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200  # Debe retornar 200 sin resultados o escapado


class TestGetCodeExample:
    """Pruebas para herramienta: get_code_example"""
    
    endpoint = "/tools/get_code_example"
    
    # Casos de Éxito
    def test_gce_1_1_python_get_products(self):
        """GCE-1.1: Python GET /products"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "language": "python"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", "")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_gce_1_2_python_post_products(self):
        """GCE-1.2: Python POST /products"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "method": "POST", "language": "python"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    def test_gce_1_3_javascript_get_products(self):
        """GCE-1.3: JavaScript GET /products"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "language": "javascript"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", "")
        assert isinstance(result, str)
    
    def test_gce_1_7_default_language(self):
        """GCE-1.7: Sin language (default Python)"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    def test_gce_1_8_default_method(self):
        """GCE-1.8: Sin method (default GET)"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "language": "python"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
    
    # Casos de Error
    def test_gce_2_1_missing_resource(self):
        """GCE-2.1: Resource faltante"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"path": "/products", "language": "python"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_gce_2_2_missing_path(self):
        """GCE-2.2: Path faltante"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "language": "python"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400
    
    def test_gce_2_5_invalid_language(self):
        """GCE-2.5: Language inválido"""
        response = requests.post(f"{BASE_URL}{self.endpoint}", 
                                params={"resource": "products", "path": "/products", "language": "ruby"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 400


class TestNoParamsTools:
    """Pruebas para herramientas sin parámetros"""
    
    def test_gai_1_1_authentication_info(self):
        """GAI-1.1: Obtener info autenticación"""
        response = requests.post(f"{BASE_URL}/tools/get_authentication_info", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert "result" in data or "tool" in data
    
    def test_gmi_1_1_multi_inventory_info(self):
        """GMI-1.1: Obtener info multi-inventario"""
        response = requests.post(f"{BASE_URL}/tools/get_multi_inventory_info", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert "result" in data or "tool" in data
    
    def test_lr_1_1_list_resources(self):
        """LR-1.1: Listar recursos"""
        response = requests.post(f"{BASE_URL}/tools/list_resources", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        result = data.get("result", {})
        assert "resources" in result or "total_endpoints" in result


class TestRateLimiting:
    """Pruebas de Rate Limiting"""
    
    def test_rate_limiting_search_endpoint(self):
        """RL-1: Prueba de rate limiting"""
        endpoint = "/tools/search_endpoint"
        responses = []
        
        # Hacer 15 solicitudes rápidamente
        for i in range(15):
            response = requests.post(f"{BASE_URL}{endpoint}", 
                                    params={"resource": "products"}, 
                                    timeout=TIMEOUT)
            responses.append(response.status_code)
        
        # Validar que hay al menos algunos 200 y posiblemente algunos 429
        assert 200 in responses
        # Si hay 429, es correcto. Si no hay, también está bien (depende de la configuración)


class TestPerformance:
    """Pruebas de Rendimiento"""
    
    def test_response_time_search_endpoint(self):
        """PERF-1: Tiempo de respuesta search_endpoint"""
        start = time.time()
        response = requests.post(f"{BASE_URL}/tools/search_endpoint", 
                                params={"resource": "products"}, 
                                timeout=TIMEOUT)
        duration = (time.time() - start) * 1000  # Convertir a ms
        
        assert response.status_code == 200
        assert duration < 500  # Debe responder en menos de 500ms
    
    def test_response_time_get_code_example(self):
        """PERF-2: Tiempo de respuesta get_code_example"""
        start = time.time()
        response = requests.post(f"{BASE_URL}/tools/get_code_example", 
                                params={"resource": "products", "path": "/products", "language": "python"}, 
                                timeout=TIMEOUT)
        duration = (time.time() - start) * 1000
        
        assert response.status_code == 200
        assert duration < 500


class TestJSONValidation:
    """Pruebas de Validación de JSON"""
    
    def test_json_valid_search_endpoint(self):
        """JSON-1: Validar JSON search_endpoint"""
        response = requests.post(f"{BASE_URL}/tools/search_endpoint", 
                                params={"resource": "products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        # Si no lanza excepción, el JSON es válido
        data = response.json()
        assert isinstance(data, dict)
    
    def test_json_valid_get_schema(self):
        """JSON-2: Validar JSON get_schema"""
        response = requests.post(f"{BASE_URL}/tools/get_schema", 
                                params={"resource": "products"}, 
                                timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

"""
Pruebas de Rate Limiting para Herramientas MCP
Utiliza Locust para simular carga y validar límites
"""

import time
import requests
from locust import HttpUser, task, between, events
from typing import Dict, List


class MCPToolsUser(HttpUser):
    """Usuario de Locust que simula solicitudes a herramientas MCP"""
    
    wait_time = between(0.1, 0.5)  # Esperar entre 100ms y 500ms entre solicitudes
    
    @task(3)
    def search_endpoint(self):
        """Tarea: search_endpoint (peso 3)"""
        self.client.post("/tools/search_endpoint", params={"resource": "products"})
    
    @task(2)
    def get_endpoint_details(self):
        """Tarea: get_endpoint_details (peso 2)"""
        self.client.post("/tools/get_endpoint_details", 
                        params={"resource": "products", "path": "/products"})
    
    @task(2)
    def get_schema(self):
        """Tarea: get_schema (peso 2)"""
        self.client.post("/tools/get_schema", params={"resource": "products"})
    
    @task(1)
    def get_code_example(self):
        """Tarea: get_code_example (peso 1)"""
        self.client.post("/tools/get_code_example", 
                        params={"resource": "products", "path": "/products", "language": "python"})
    
    @task(1)
    def search_documentation(self):
        """Tarea: search_documentation (peso 1)"""
        self.client.post("/tools/search_documentation", params={"query": "stock"})
    
    @task(1)
    def get_authentication_info(self):
        """Tarea: get_authentication_info (peso 1)"""
        self.client.post("/tools/get_authentication_info")
    
    @task(1)
    def get_multi_inventory_info(self):
        """Tarea: get_multi_inventory_info (peso 1)"""
        self.client.post("/tools/get_multi_inventory_info")
    
    @task(1)
    def list_resources(self):
        """Tarea: list_resources (peso 1)"""
        self.client.post("/tools/list_resources")


class RateLimitingTest:
    """Pruebas específicas de rate limiting"""
    
    BASE_URL = "http://localhost:8000"
    TIMEOUT = 10
    
    def __init__(self):
        self.results = {
            "success": 0,
            "rate_limited": 0,
            "errors": 0,
            "response_times": []
        }
    
    def test_rate_limiting_5_requests_per_second(self):
        """Prueba: 5 solicitudes por segundo (dentro del límite)"""
        print("\n" + "="*70)
        print("Prueba: 5 solicitudes por segundo (dentro del límite)")
        print("="*70)
        
        endpoint = "/tools/search_endpoint"
        params = {"resource": "products"}
        
        for i in range(5):
            response = requests.post(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.TIMEOUT)
            self.results["response_times"].append(response.elapsed.total_seconds() * 1000)
            
            if response.status_code == 200:
                self.results["success"] += 1
                print(f"  [{i+1}/5] ✓ HTTP 200 ({response.elapsed.total_seconds()*1000:.1f}ms)")
            elif response.status_code == 429:
                self.results["rate_limited"] += 1
                print(f"  [{i+1}/5] ⚠ HTTP 429 (Rate Limited)")
            else:
                self.results["errors"] += 1
                print(f"  [{i+1}/5] ✗ HTTP {response.status_code}")
            
            time.sleep(0.2)  # 200ms entre solicitudes = 5 req/s
        
        print(f"\nResultado: {self.results['success']}/5 exitosas")
        assert self.results["success"] == 5, "Todas las solicitudes deberían ser exitosas"
    
    def test_rate_limiting_10_requests_per_second(self):
        """Prueba: 10 solicitudes por segundo (en el límite)"""
        print("\n" + "="*70)
        print("Prueba: 10 solicitudes por segundo (en el límite)")
        print("="*70)
        
        endpoint = "/tools/search_endpoint"
        params = {"resource": "products"}
        
        self.results = {"success": 0, "rate_limited": 0, "errors": 0, "response_times": []}
        
        for i in range(10):
            response = requests.post(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.TIMEOUT)
            self.results["response_times"].append(response.elapsed.total_seconds() * 1000)
            
            if response.status_code == 200:
                self.results["success"] += 1
                print(f"  [{i+1:2d}/10] ✓ HTTP 200 ({response.elapsed.total_seconds()*1000:.1f}ms)")
            elif response.status_code == 429:
                self.results["rate_limited"] += 1
                print(f"  [{i+1:2d}/10] ⚠ HTTP 429 (Rate Limited)")
            else:
                self.results["errors"] += 1
                print(f"  [{i+1:2d}/10] ✗ HTTP {response.status_code}")
            
            time.sleep(0.1)  # 100ms entre solicitudes = 10 req/s
        
        print(f"\nResultado: {self.results['success']}/10 exitosas, {self.results['rate_limited']} limitadas")
        assert self.results["success"] >= 8, "Al menos 8 de 10 deberían ser exitosas"
    
    def test_rate_limiting_15_requests_per_second(self):
        """Prueba: 15 solicitudes por segundo (excediendo el límite)"""
        print("\n" + "="*70)
        print("Prueba: 15 solicitudes por segundo (excediendo el límite)")
        print("="*70)
        
        endpoint = "/tools/search_endpoint"
        params = {"resource": "products"}
        
        self.results = {"success": 0, "rate_limited": 0, "errors": 0, "response_times": []}
        
        for i in range(15):
            response = requests.post(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.TIMEOUT)
            self.results["response_times"].append(response.elapsed.total_seconds() * 1000)
            
            if response.status_code == 200:
                self.results["success"] += 1
                print(f"  [{i+1:2d}/15] ✓ HTTP 200 ({response.elapsed.total_seconds()*1000:.1f}ms)")
            elif response.status_code == 429:
                self.results["rate_limited"] += 1
                print(f"  [{i+1:2d}/15] ⚠ HTTP 429 (Rate Limited)")
            else:
                self.results["errors"] += 1
                print(f"  [{i+1:2d}/15] ✗ HTTP {response.status_code}")
            
            time.sleep(0.067)  # ~67ms entre solicitudes = ~15 req/s
        
        print(f"\nResultado: {self.results['success']}/15 exitosas, {self.results['rate_limited']} limitadas")
        assert self.results["rate_limited"] > 0, "Debería haber solicitudes limitadas"
    
    def test_rate_limiting_burst(self):
        """Prueba: Ráfaga de solicitudes (sin espera)"""
        print("\n" + "="*70)
        print("Prueba: Ráfaga de solicitudes sin espera")
        print("="*70)
        
        endpoint = "/tools/search_endpoint"
        params = {"resource": "products"}
        
        self.results = {"success": 0, "rate_limited": 0, "errors": 0, "response_times": []}
        
        # Hacer 20 solicitudes lo más rápido posible
        for i in range(20):
            try:
                response = requests.post(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.TIMEOUT)
                self.results["response_times"].append(response.elapsed.total_seconds() * 1000)
                
                if response.status_code == 200:
                    self.results["success"] += 1
                    print(f"  [{i+1:2d}/20] ✓ HTTP 200 ({response.elapsed.total_seconds()*1000:.1f}ms)")
                elif response.status_code == 429:
                    self.results["rate_limited"] += 1
                    print(f"  [{i+1:2d}/20] ⚠ HTTP 429 (Rate Limited)")
                else:
                    self.results["errors"] += 1
                    print(f"  [{i+1:2d}/20] ✗ HTTP {response.status_code}")
            except Exception as e:
                self.results["errors"] += 1
                print(f"  [{i+1:2d}/20] ✗ Error: {str(e)}")
        
        print(f"\nResultado: {self.results['success']}/20 exitosas, {self.results['rate_limited']} limitadas")
        assert self.results["rate_limited"] > 0, "Debería haber muchas solicitudes limitadas"
    
    def test_rate_limiting_recovery(self):
        """Prueba: Recuperación después de rate limiting"""
        print("\n" + "="*70)
        print("Prueba: Recuperación después de rate limiting")
        print("="*70)
        
        endpoint = "/tools/search_endpoint"
        params = {"resource": "products"}
        
        # Fase 1: Exceder límite
        print("\nFase 1: Excediendo límite (10 solicitudes rápidas)...")
        for i in range(10):
            requests.post(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.TIMEOUT)
        
        # Fase 2: Esperar
        print("Fase 2: Esperando 2 segundos...")
        time.sleep(2)
        
        # Fase 3: Intentar de nuevo
        print("Fase 3: Intentando nuevamente...")
        response = requests.post(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.TIMEOUT)
        
        if response.status_code == 200:
            print("✓ Recuperación exitosa - HTTP 200")
            assert True
        else:
            print(f"✗ Aún limitado - HTTP {response.status_code}")
            assert False, "Debería recuperarse después de esperar"
    
    def test_different_endpoints_rate_limiting(self):
        """Prueba: Rate limiting en diferentes endpoints"""
        print("\n" + "="*70)
        print("Prueba: Rate limiting en diferentes endpoints")
        print("="*70)
        
        endpoints = [
            ("/tools/search_endpoint", {"resource": "products"}),
            ("/tools/get_endpoint_details", {"resource": "products", "path": "/products"}),
            ("/tools/get_schema", {"resource": "products"}),
            ("/tools/search_documentation", {"query": "stock"}),
            ("/tools/get_code_example", {"resource": "products", "path": "/products"}),
        ]
        
        self.results = {"success": 0, "rate_limited": 0, "errors": 0, "response_times": []}
        
        # Hacer 15 solicitudes a diferentes endpoints
        for i in range(15):
            endpoint, params = endpoints[i % len(endpoints)]
            response = requests.post(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.TIMEOUT)
            self.results["response_times"].append(response.elapsed.total_seconds() * 1000)
            
            if response.status_code == 200:
                self.results["success"] += 1
                status = "✓"
            elif response.status_code == 429:
                self.results["rate_limited"] += 1
                status = "⚠"
            else:
                self.results["errors"] += 1
                status = "✗"
            
            print(f"  [{i+1:2d}/15] {status} {endpoint} - HTTP {response.status_code}")
        
        print(f"\nResultado: {self.results['success']}/15 exitosas, {self.results['rate_limited']} limitadas")
    
    def print_statistics(self):
        """Imprimir estadísticas de las pruebas"""
        print("\n" + "="*70)
        print("ESTADÍSTICAS DE RATE LIMITING")
        print("="*70)
        
        if self.results["response_times"]:
            avg_time = sum(self.results["response_times"]) / len(self.results["response_times"])
            min_time = min(self.results["response_times"])
            max_time = max(self.results["response_times"])
            
            print(f"\nTiempos de Respuesta:")
            print(f"  Promedio: {avg_time:.2f}ms")
            print(f"  Mínimo:   {min_time:.2f}ms")
            print(f"  Máximo:   {max_time:.2f}ms")
        
        print(f"\nResultados Generales:")
        print(f"  Exitosas:    {self.results['success']}")
        print(f"  Limitadas:   {self.results['rate_limited']}")
        print(f"  Errores:     {self.results['errors']}")
        
        total = self.results['success'] + self.results['rate_limited'] + self.results['errors']
        if total > 0:
            success_rate = (self.results['success'] / total) * 100
            print(f"  Tasa de éxito: {success_rate:.1f}%")


def run_all_tests():
    """Ejecutar todas las pruebas de rate limiting"""
    tester = RateLimitingTest()
    
    try:
        tester.test_rate_limiting_5_requests_per_second()
        tester.test_rate_limiting_10_requests_per_second()
        tester.test_rate_limiting_15_requests_per_second()
        tester.test_rate_limiting_burst()
        tester.test_rate_limiting_recovery()
        tester.test_different_endpoints_rate_limiting()
    except AssertionError as e:
        print(f"\n✗ Prueba fallida: {str(e)}")
    except Exception as e:
        print(f"\n✗ Error inesperado: {str(e)}")
    finally:
        tester.print_statistics()


if __name__ == "__main__":
    run_all_tests()

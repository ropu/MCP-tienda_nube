# Ejemplos de Código - API Tienda Nube

## Autenticación

Todos los ejemplos requieren un token de acceso Bearer.

```python
import requests

API_BASE_URL = "https://api.tiendanube.com/v1"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
```

## Productos

### Listar Productos

```python
import requests

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
params = {
    "page": 1,
    "per_page": 30,
    "sort_by": "price-ascending"
}

response = requests.get(f"{API_BASE_URL}/products", headers=headers, params=params)
products = response.json()

for product in products:
    print(f"ID: {product['id']}, Nombre: {product['name']['es']}")
```

### Obtener Producto por ID

```python
product_id = 1234

response = requests.get(f"{API_BASE_URL}/products/{product_id}", headers=headers)
product = response.json()

print(f"Producto: {product['name']['es']}")
for variant in product['variants']:
    print(f"  SKU: {variant['sku']}, Precio: ${variant['price']}")
```

### Obtener Producto por SKU

```python
sku = "BSG1234A"

response = requests.get(f"{API_BASE_URL}/products/sku/{sku}", headers=headers)
product = response.json()

print(f"Producto encontrado: {product['name']['es']}")
```

### Crear Producto

```python
import json

product_data = {
    "name": {
        "es": "Master Ball",
        "en": "Master Ball"
    },
    "description": {
        "es": "<p>La mejor bola de Pokémon</p>",
        "en": "<p>The best Pokémon ball</p>"
    },
    "attributes": [
        {
            "es": "Tamaño",
            "en": "Size"
        }
    ],
    "variants": [
        {
            "values": [
                {"es": "Pequeño", "en": "Small"}
            ],
            "price": "25.00",
            "promotional_price": "19.00",
            "cost": "10.00",
            "sku": "MB-S",
            "inventory_levels": [
                {
                    "location_id": "01GQ2ZHK064BQRHGDB7CCV0Y6N",
                    "stock": 100
                }
            ]
        },
        {
            "values": [
                {"es": "Mediano", "en": "Medium"}
            ],
            "price": "30.00",
            "promotional_price": "24.00",
            "cost": "12.00",
            "sku": "MB-M",
            "inventory_levels": [
                {
                    "location_id": "01GQ2ZHK064BQRHGDB7CCV0Y6N",
                    "stock": 150
                }
            ]
        }
    ],
    "published": True,
    "free_shipping": False,
    "tags": "pokemon,balls,juguetes"
}

response = requests.post(
    f"{API_BASE_URL}/products",
    headers=headers,
    data=json.dumps(product_data)
)

if response.status_code == 201:
    new_product = response.json()
    print(f"Producto creado con ID: {new_product['id']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Actualizar Stock (Multi-Inventario)

```python
import json

stock_update = [
    {
        "id": 1234,
        "variants": [
            {
                "id": 101,
                "inventory_levels": [
                    {
                        "location_id": "01GQ2ZHK064BQRHGDB7CCV0Y6N",
                        "stock": 50
                    }
                ]
            }
        ]
    }
]

response = requests.patch(
    f"{API_BASE_URL}/products/stock-price",
    headers=headers,
    data=json.dumps(stock_update)
)

if response.status_code == 200:
    print("Stock actualizado correctamente")
else:
    print(f"Error: {response.status_code}")
```

### Actualizar Precio y Stock

```python
import json

update_data = [
    {
        "id": 1234,
        "variants": [
            {
                "id": 101,
                "price": "28.00",
                "promotional_price": "22.00",
                "cost": "11.00",
                "inventory_levels": [
                    {
                        "location_id": "01GQ2ZHK064BQRHGDB7CCV0Y6N",
                        "stock": 75
                    }
                ]
            }
        ]
    }
]

response = requests.patch(
    f"{API_BASE_URL}/products/stock-price",
    headers=headers,
    data=json.dumps(update_data)
)

if response.status_code == 200:
    print("Precio y stock actualizados")
else:
    print(f"Error: {response.status_code}")
```

### Eliminar Producto

```python
product_id = 1234

response = requests.delete(f"{API_BASE_URL}/products/{product_id}", headers=headers)

if response.status_code == 204:
    print("Producto eliminado")
else:
    print(f"Error: {response.status_code}")
```

## Órdenes

### Listar Órdenes

```python
params = {
    "status": "open",
    "payment_status": "paid",
    "page": 1,
    "per_page": 30
}

response = requests.get(f"{API_BASE_URL}/orders", headers=headers, params=params)
orders = response.json()

for order in orders:
    print(f"Orden #{order['number']}: ${order['total']} - {order['status']}")
```

### Obtener Orden por ID

```python
order_id = 871254203

response = requests.get(f"{API_BASE_URL}/orders/{order_id}", headers=headers)
order = response.json()

print(f"Orden #{order['number']}")
print(f"Cliente: {order['contact_email']}")
print(f"Total: ${order['total']}")
print(f"Estado: {order['status']}")
print(f"Estado de pago: {order['payment_status']}")
print(f"\nProductos:")
for product in order['products']:
    print(f"  - {product['name']}: {product['quantity']} x ${product['price']}")
```

### Crear Orden

```python
import json

order_data = {
    "contact_email": "customer@example.com",
    "contact_phone": "+1234567890",
    "contact_identification": "12345678901",
    "billing_name": "John Doe",
    "billing_address": "123 Main St",
    "billing_city": "New York",
    "billing_province": "NY",
    "billing_country": "US",
    "shipping_address": {
        "name": "John Doe",
        "address": "123 Main St",
        "city": "New York",
        "province": "NY",
        "zipcode": "10001",
        "country": "US"
    },
    "products": [
        {
            "product_id": 1234,
            "variant_id": 101,
            "quantity": 2
        }
    ],
    "note": "Please deliver in the morning",
    "owner_note": "VIP customer"
}

response = requests.post(
    f"{API_BASE_URL}/orders",
    headers=headers,
    data=json.dumps(order_data)
)

if response.status_code == 201:
    new_order = response.json()
    print(f"Orden creada: #{new_order['number']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Actualizar Orden

```python
import json

order_id = 871254203

update_data = {
    "note": "Updated customer note",
    "owner_note": "Updated owner note"
}

response = requests.put(
    f"{API_BASE_URL}/orders/{order_id}",
    headers=headers,
    data=json.dumps(update_data)
)

if response.status_code == 200:
    print("Orden actualizada")
else:
    print(f"Error: {response.status_code}")
```

### Marcar Orden como Pagada

```python
order_id = 871254203

response = requests.post(
    f"{API_BASE_URL}/orders/{order_id}/pay",
    headers=headers
)

if response.status_code == 200:
    print("Orden marcada como pagada")
else:
    print(f"Error: {response.status_code}")
```

### Cerrar Orden

```python
order_id = 871254203

response = requests.post(
    f"{API_BASE_URL}/orders/{order_id}/close",
    headers=headers
)

if response.status_code == 200:
    print("Orden cerrada")
else:
    print(f"Error: {response.status_code}")
```

### Cancelar Orden

```python
import json

order_id = 871254203

cancel_data = {
    "reason": "inventory"  # customer, fraud, inventory, other
}

response = requests.post(
    f"{API_BASE_URL}/orders/{order_id}/cancel",
    headers=headers,
    data=json.dumps(cancel_data)
)

if response.status_code == 200:
    print("Orden cancelada")
else:
    print(f"Error: {response.status_code}")
```

### Obtener Historial de Valores de Orden

```python
order_id = 871254203

response = requests.get(
    f"{API_BASE_URL}/orders/{order_id}/history/values",
    headers=headers
)

history = response.json()

for entry in history:
    print(f"Cambio: {entry['field']} de {entry['old_value']} a {entry['new_value']}")
```

### Obtener Historial de Ediciones de Orden

```python
order_id = 871254203

response = requests.get(
    f"{API_BASE_URL}/orders/{order_id}/history/editions",
    headers=headers
)

editions = response.json()

for edition in editions:
    print(f"Edición: {edition['edited_at']} por {edition['editor']}")
```

## Búsqueda Avanzada

### Buscar Productos por Criterios

```python
params = {
    "q": "Master Ball",  # Búsqueda por nombre
    "published": "true",
    "min_stock": 10,
    "max_stock": 1000,
    "has_promotional_price": "true",
    "sort_by": "price-ascending",
    "page": 1,
    "per_page": 50,
    "fields": "id,name,price,stock"
}

response = requests.get(f"{API_BASE_URL}/products", headers=headers, params=params)
products = response.json()

print(f"Encontrados: {len(products)} productos")
```

### Buscar Órdenes por Rango de Fechas

```python
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(days=1)).isoformat()
today = datetime.now().isoformat()

params = {
    "created_at_min": yesterday,
    "created_at_max": today,
    "status": "open",
    "page": 1,
    "per_page": 100
}

response = requests.get(f"{API_BASE_URL}/orders", headers=headers, params=params)
orders = response.json()

print(f"Órdenes de hoy: {len(orders)}")
```

## Manejo de Errores

```python
import requests

try:
    response = requests.get(
        f"{API_BASE_URL}/products/1234",
        headers=headers,
        timeout=10
    )
    
    # Verificar código de estado
    if response.status_code == 200:
        product = response.json()
        print(f"Producto: {product['name']['es']}")
    elif response.status_code == 404:
        print("Producto no encontrado")
    elif response.status_code == 401:
        print("Token inválido o expirado")
    elif response.status_code == 429:
        print("Límite de rate limit alcanzado")
    else:
        print(f"Error {response.status_code}: {response.text}")
        
except requests.exceptions.Timeout:
    print("Timeout: La solicitud tardó demasiado")
except requests.exceptions.ConnectionError:
    print("Error de conexión")
except Exception as e:
    print(f"Error inesperado: {e}")
```

## Tips y Mejores Prácticas

1. **Siempre usa paginación** para listas grandes
2. **Cachea resultados** cuando sea posible
3. **Usa campos específicos** con el parámetro `fields` para reducir datos
4. **Maneja reintentos** para errores de red
5. **Respeta los límites de rate limit**
6. **Usa la nueva API de multi-inventario** para productos
7. **Valida datos** antes de enviar a la API

---

Para más información, consulta la documentación oficial:
https://tiendanube.github.io/api-documentation/

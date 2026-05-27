# is4460-api-hw-flower-supplier
This repo holds a dataset of bulk flowers that a flower shop can order. 

## Flower Supplier API

This is a small Django API for a flower shop supplier inventory.

### Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The migration includes a few starter inventory rows so the API is usable right
away.

### Inventory model

Each inventory item has:

- `type_of_flower`
- `description`
- `quantity`
- `cost`

### API

Swagger docs are available after starting the server:

```bash
http://127.0.0.1:8000/swagger/
```

The raw OpenAPI schema is available at:

```bash
http://127.0.0.1:8000/swagger.json
```

List all available bulk inventory:

```bash
curl http://127.0.0.1:8000/inventory/
```

Purchase flowers from inventory:

```bash
curl -X POST http://127.0.0.1:8000/inventory/ \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "quantity": 12}'
```

Use an `id` from the list response. The purchase endpoint subtracts the purchased
quantity from inventory and returns the purchased item.

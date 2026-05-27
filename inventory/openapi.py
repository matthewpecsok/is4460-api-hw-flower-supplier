OPENAPI_SCHEMA = {
    "openapi": "3.0.3",
    "info": {
        "title": "Flower Supplier API",
        "version": "1.0.0",
        "description": "A simple API for viewing and purchasing bulk flower inventory.",
    },
    "servers": [{"url": "/"}],
    "tags": [
        {
            "name": "Inventory",
            "description": "Bulk flower inventory available for purchase.",
        }
    ],
    "paths": {
        "/inventory/": {
            "get": {
                "tags": ["Inventory"],
                "summary": "List available flower inventory",
                "description": "Returns every bulk flower item currently available from the supplier.",
                "responses": {
                    "200": {
                        "description": "Inventory list returned successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/InventoryListResponse"
                                },
                                "example": {
                                    "inventory": [
                                        {
                                            "id": 1,
                                            "type_of_flower": "Rose",
                                            "description": (
                                                "Classic long-stem roses for bouquets, "
                                                "arrangements, and events."
                                            ),
                                            "quantity": 250,
                                            "cost": "2.50",
                                        }
                                    ]
                                },
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Inventory"],
                "summary": "Purchase flowers from inventory",
                "description": (
                    "Purchases a quantity of one flower inventory item. "
                    "The API subtracts the purchased quantity from available inventory "
                    "and returns the purchased item with the remaining quantity."
                ),
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PurchaseRequest"
                            },
                            "example": {"id": 1, "quantity": 12},
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Purchase completed successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/PurchaseResponse"
                                },
                                "example": {
                                    "purchased": {
                                        "id": 1,
                                        "type_of_flower": "Rose",
                                        "description": (
                                            "Classic long-stem roses for bouquets, "
                                            "arrangements, and events."
                                        ),
                                        "quantity": 238,
                                        "cost": "2.50",
                                        "purchased_quantity": 12,
                                        "purchase_total": "30.00",
                                    }
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Invalid request or not enough inventory.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                                "example": {
                                    "error": "Not enough flowers available for that purchase."
                                },
                            }
                        },
                    },
                    "404": {
                        "description": "Inventory item not found.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                                "example": {"error": "Inventory item not found."},
                            }
                        },
                    },
                    "405": {
                        "description": "Unsupported HTTP method.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                                "example": {"error": "Use GET or POST."},
                            }
                        },
                    },
                },
            },
        }
    },
    "components": {
        "schemas": {
            "FlowerInventoryItem": {
                "type": "object",
                "required": [
                    "id",
                    "type_of_flower",
                    "description",
                    "quantity",
                    "cost",
                ],
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 1,
                    },
                    "type_of_flower": {
                        "type": "string",
                        "example": "Rose",
                    },
                    "description": {
                        "type": "string",
                        "example": (
                            "Classic long-stem roses for bouquets, arrangements, "
                            "and events."
                        ),
                    },
                    "quantity": {
                        "type": "integer",
                        "minimum": 0,
                        "example": 250,
                    },
                    "cost": {
                        "type": "string",
                        "format": "decimal",
                        "example": "2.50",
                    },
                },
            },
            "PurchasedFlowerInventoryItem": {
                "allOf": [
                    {"$ref": "#/components/schemas/FlowerInventoryItem"},
                    {
                        "type": "object",
                        "required": ["purchased_quantity", "purchase_total"],
                        "properties": {
                            "purchased_quantity": {
                                "type": "integer",
                                "minimum": 1,
                                "example": 12,
                            },
                            "purchase_total": {
                                "type": "string",
                                "format": "decimal",
                                "example": "30.00",
                            },
                        },
                    },
                ]
            },
            "InventoryListResponse": {
                "type": "object",
                "required": ["inventory"],
                "properties": {
                    "inventory": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/FlowerInventoryItem"},
                    }
                },
            },
            "PurchaseRequest": {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Inventory item id from the GET /inventory/ response.",
                        "example": 1,
                    },
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                        "default": 1,
                        "description": "Number of flowers to purchase.",
                        "example": 12,
                    },
                },
            },
            "PurchaseResponse": {
                "type": "object",
                "required": ["purchased"],
                "properties": {
                    "purchased": {
                        "$ref": "#/components/schemas/PurchasedFlowerInventoryItem"
                    }
                },
            },
            "ErrorResponse": {
                "type": "object",
                "required": ["error"],
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Inventory item not found.",
                    }
                },
            },
        }
    },
}


SWAGGER_UI_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flower Supplier API Docs</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function () {
      SwaggerUIBundle({
        url: "/swagger.json",
        dom_id: "#swagger-ui"
      });
    };
  </script>
</body>
</html>
"""

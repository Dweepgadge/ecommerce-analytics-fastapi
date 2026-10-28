from fastapi.testclient import TestClient
from main import app

# TestClient hamari FastAPI app ko bina browser ke test karne deta hai
client = TestClient(app)


# ----------------- TEST 1: PUBLIC ORDERS ROUTE -----------------
def test_get_orders():
    # GET request bhejo
    response = client.get("/orders/")
    
    # Check karo: Status 200 OK aana chahiye
    assert response.status_code == 200
    
    # Check karo: Response JSON hona chahiye aur usme 'total_count' hona chahiye
    data = response.json()
    assert "total_count" in data
    assert "data" in data


# ----------------- TEST 2: SECURITY TEST (Bina Token ke Order Create karna) -----------------
def test_create_order_unauthorized():
    # Bina token ke naya order bhejne ki koshish karo
    new_order = {
        "product_name": "Test Phone",
        "price": 15000,
        "quantity": 1
    }
    response = client.post("/orders/", json=new_order)
    
    # Security Rule: Token na hone par 401 Unauthorized aana chahiye!
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# ----------------- TEST 3: INVALID DATA TEST (Pydantic Validation Check) -----------------
def test_invalid_order_id_404():
    # Ek aisi order ID dhundo jo database me nahi hai (e.g. 999999)
    response = client.get("/orders/999999")
    
    # 404 Not Found aana chahiye!
    assert response.status_code == 404
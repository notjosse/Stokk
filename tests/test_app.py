
def test_always_true():
    assert True

def test_login(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_register(client):
    response = client.get("/register")
    assert response.status_code == 200
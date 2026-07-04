import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "PCBMind AI"
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_docs(client):
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_and_login(client):
    register_resp = await client.post("/api/v1/auth/register", json={
        "email": "test@pcbmind.ai",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
    })
    assert register_resp.status_code == 201
    data = register_resp.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@pcbmind.ai"

    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "test@pcbmind.ai",
        "password": "testpass123",
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


@pytest.mark.asyncio
async def test_register_duplicate(client):
    await client.post("/api/v1/auth/register", json={
        "email": "dup@pcbmind.ai",
        "username": "dupuser",
        "password": "testpass123",
    })
    resp = await client.post("/api/v1/auth/register", json={
        "email": "dup@pcbmind.ai",
        "username": "dupuser2",
        "password": "testpass123",
    })
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_login_invalid(client):
    resp = await client.post("/api/v1/auth/login", json={
        "email": "nonexistent@pcbmind.ai",
        "password": "wrongpass",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_protected_route(client):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 403 or resp.status_code == 401


@pytest.mark.asyncio
async def test_projects_unauthorized(client):
    resp = await client.get("/api/v1/projects")
    assert resp.status_code == 403 or resp.status_code == 401

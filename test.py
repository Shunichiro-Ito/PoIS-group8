# pytest test.py

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import pytest

from main import app

client = TestClient(app)
credentials1 = ("jessica", "toEncode")
credentials2 = ("johndoe", "toEncode")

@pytest.fixture
async def async_client():
  """Fixture to create a FastAPI test client."""
  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_test_client:
      yield async_test_client

@pytest.mark.anyio
async def test_login(async_client: AsyncClient):

    form_data = {"username": "johndoe","password": "toEncode"}
    response = await async_client.post(  
        "/users/token", 
        data=form_data,
        headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == 200

# Unit Testing Standards (pytest-asyncio)
1. **Framework**: Use `pytest` and `pytest-asyncio` (`@pytest.mark.asyncio`).
2. **Client**: Use `httpx.AsyncClient` alongside FastAPI's `TestClient`.
3. **Mocking**: NEVER hit the real database in unit tests. Use `unittest.mock.MagicMock`.
4. **Coverage**: Ensure tests cover both Happy Path and validation errors (422).
5. **Fixtures**: Define reusable fixtures in `conftest.py`.
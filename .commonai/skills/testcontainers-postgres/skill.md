# Integration Testing Standards (Testcontainers)
1. **Framework**: Use `testcontainers-python`. 
2. **Lifecycle**: Spin up `PostgresContainer("postgres:15-alpine")` as a pytest fixture.
3. **Database URL**: Override FastAPI `get_db` to point to `container.get_connection_url()`.
4. **Migrations**: Apply Alembic migrations to the transient container before tests.
5. **Isolation**: Truncate tables between tests to prevent state leakage.
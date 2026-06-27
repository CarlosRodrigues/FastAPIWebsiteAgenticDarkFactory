# FastAPI CRUD Standards
1. **Pydantic v2**: Validate payloads using Pydantic `BaseModel`. Use `ConfigDict(from_attributes=True)`.
2. **Async Execution**: All route handlers must be `async def`.
3. **Dependency Injection**: Inject database sessions via `Depends(get_db)`.
4. **Routing**: Group routes using `APIRouter`.
5. **Error Handling**: Raise `HTTPException` with proper 4xx/5xx status codes.
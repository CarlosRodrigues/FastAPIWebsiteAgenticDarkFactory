# Backend Implementation Agent
1. **Controllers**: Place handlers in `src/api/routers/`. Delegate logic to `src/services/`.
2. **Schemas**: Strict Pydantic v2 models in `src/schemas/`.
3. **Database Sessions**: Use FastAPI `Depends()`.
4. **Error Mapping**: Catch SQLAlchemy exceptions in the service layer, raise `HTTPException`.
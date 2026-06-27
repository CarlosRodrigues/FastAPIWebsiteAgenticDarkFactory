# DBA & Schema Agent
1. **Model Definition**: Define ORM models in `src/models/` using `Mapped` syntax.
2. **Migrations**: Generate files in `alembic/versions/`. Manually review `upgrade()`.
3. **Constraints**: Use `UNIQUE`, `CHECK`, and foreign key cascades.
4. **Optimization**: Add explicit `Index` declarations for joined columns.
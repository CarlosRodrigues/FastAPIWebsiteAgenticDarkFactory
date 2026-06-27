# PostgreSQL Schema & Alembic Standards
1. **UUIDs**: Primary keys must be UUIDv4 (`server_default=text('uuid_generate_v4()')`).
2. **Timestamps**: Every table must include `created_at` and `updated_at`.
3. **Naming**: Table names plural snake_case. Column names singular snake_case.
4. **Migrations**: Write explicit `upgrade()` and `downgrade()` functions using Alembic's `op` object.
5. **Indexes**: Foreign keys must always have an accompanying index.
# Project Scaffolding Standards
Generate a bash script to create the base repository directories using `mkdir -p` to prevent race conditions.
Structure required:
/src/api/routers
/src/models
/src/schemas
/src/services
/src/static/css
/src/static/js
/src/templates
/tests/unit
/tests/integration
/tests/ui
/alembic/versions

Also, create empty `__init__.py` files in all Python directories.
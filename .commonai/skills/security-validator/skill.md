# Security & Anti-Pattern Validator
Reject the diff (output VALIDATION_FAILED) if you find:
1. **SQL Injection**: Raw SQL queries.
2. **Auth Bypass**: Endpoints lacking proper guards.
3. **Secret Leakage**: Hardcoded passwords or JWT secrets.
4. **N+1 Queries**: SQLAlchemy loops without `joinedload`.
5. **Mass Assignment**: Endpoints accepting raw dictionaries into DB models.
If clean, output "PASS".
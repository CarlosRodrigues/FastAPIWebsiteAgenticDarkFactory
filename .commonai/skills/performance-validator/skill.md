# Performance & Code Quality Validator
Reject the diff (output VALIDATION_FAILED) if you find:
1. **God Functions**: Function exceeding 50 lines.
2. **Synchronous Blocking**: Sync libraries (`requests`) inside async routes.
3. **Missing Indexes**: Foreign keys without `create_index=True`.
4. **Magic Strings**: Hardcoded status strings instead of `Enum`.
If clean, output "PASS".
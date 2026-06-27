# UI Testing Standards (Playwright)
1. **Framework**: Use `pytest-playwright` for E2E testing.
2. **Selectors**: ALWAYS prefer `getByRole`, `getByLabel`, or `getByTestId`.
3. **State**: Mock API responses using `page.route()` or run against local Testcontainers.
4. **Assertions**: Use Playwright's auto-retrying assertions.
5. **Headless**: Run in headless mode by default.
# Guardrails & Footgun Prevention Guide

## Overview
This document provides a comprehensive guide to implementing **guardrails** and **footgun prevention** mechanisms in software development. It covers strategies for robust error handling, input validation, fail-safe defaults, and designing APIs/systems that prevent common misuse while preserving usability. Practical examples across multiple languages and frameworks are included.

---

## 1. Core Principles

1. **Fail-Safe Defaults** – Systems should default to the safest or most predictable state when input is missing or invalid.
2. **Explicit Over Implicit** – Require explicit choices for risky operations (e.g., deletions, overrides).
3. **Validate Early, Fail Clearly** – Catch problems at the earliest point with meaningful messages.
4. **Least Privilege** – Limit access rights to minimum necessary for functionality.
5. **Graceful Degradation** – Maintain partial functionality when possible instead of total failure.

---

## 2. Error Handling Strategies

### 2.1 Use Structured Exception Handling
- Catch specific exceptions, not generic `Exception`.
- Log sufficient context (input, state) without leaking sensitive data.
- Convert low-level errors into domain-specific messages.

**Python Example:**
```python
import logging

try:
    value = int(user_input)
except ValueError:
    logging.warning(f"Invalid integer input: {user_input}")
    raise ValueError("Input must be a valid integer.")
```

**JavaScript Example:**
```javascript
try {
  const parsed = JSON.parse(input);
} catch (err) {
  console.error('Invalid JSON:', err.message);
  throw new Error('Provided input is not valid JSON.');
}
```

### 2.2 Idempotency & Retry Safety
- Design operations so retries do not cause unintended side effects (e.g., duplicate orders).

---

## 3. Input Validation

### 3.1 Whitelist Known-Good Patterns
- Prefer whitelisting over blacklisting.
- Use schema validation (JSON Schema, Pydantic, Zod).

**Python (Pydantic) Example:**
```python
from pydantic import BaseModel, conint

class UserCreate(BaseModel):
    age: conint(gt=0, lt=150)
```

**Node.js (Zod) Example:**
```javascript
const z = require('zod');
const UserSchema = z.object({
  age: z.number().positive().max(149)
});
```

### 3.2 Sanitize Inputs
- Escape or remove dangerous characters for the execution context (SQL, HTML, shell commands).

**SQL Injection Prevention:**
- Use parameterized queries/prepared statements.

**Python (sqlite3):**
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Shell Command Safety:**
Avoid passing unsanitized input to `os.system` or `subprocess.run(shell=True)`.

---

## 4. Fail-Safe Defaults in Design

- Unset boolean flags should default to `false` for risky actions (e.g., `delete_after_processing=False`).
- Empty collections instead of `null` to avoid `NullPointerException`.
- Timeout values should have reasonable lower/upper bounds.

**Example – Safe API Defaults:**
```python
# Unsafe
def fetch_data(timeout=None): ...

# Safer
def fetch_data(timeout=30):  # seconds, bounded
    if not (1 <= timeout <= 120):
        raise ValueError("Timeout must be between 1 and 120 seconds")
```

---

## 5. Designing Misuse-Resistant APIs

### 5.1 Require Explicit Opt-In for Dangerous Operations
- Mark destructive methods with clear naming (`destroy()`, `purge_all()`).
- Require a confirmation flag or secondary authorization step.

**Python Example:**
```python
def delete_user(user_id, *, confirm=False):
    if not confirm:
        raise PermissionError("Must set confirm=True to delete user")
    ...
```

### 5.2 Immutable by Default
- Prevent accidental mutation of shared data structures.

**JavaScript Example:**
```javascript
const config = Object.freeze({debug: false});
// config.debug = true; // Throws in strict mode
```

### 5.3 Narrow Interfaces Over Broad Ones
- Expose minimal surface area needed.

---

## 6. Dangerous Patterns & Safer Alternatives

| Dangerous Pattern | Why It’s Risky | Safer Alternative |
|-------------------|----------------|--------------------|
| `eval(user_input)` | Executes arbitrary code | Parse/validate input; use safe DSL or mapping |
| String concatenation in SQL | SQL injection | Parameterized queries |
| Silent exception swallowing | Hidden bugs | Always log/handle exceptions |
| Shared mutable state without locks | Race conditions | Immutability or concurrency primitives |
| Unbounded loops/recursion | Crashes/hangs | Input size checks, limits, timeouts |

---

## 7. Framework-Specific Guidance

### 7.1 Streamlit (Python)
- Validate uploaded file types and sizes before processing.
- Wrap heavy computations in `st.spinner` with timeout guards.
- Avoid exposing raw exception tracebacks to users.

### 7.2 Web (Django/FastAPI)
- Use framework validators and serializers.
- Apply CSRF protection and rate limiting.

### 7.3 Frontend (React/Vue)
- Use controlled components to prevent invalid state.
- Sanitize user-generated content before rendering as HTML.

---

## 8. Testing Guardrails

- Write unit tests for validation logic (invalid → error, valid → accept).
- Property-based testing to explore edge cases.
- Simulate misuse scenarios (e.g., malformed payloads, unexpected sequences).

---

## 9. Monitoring & Alerting

- Track validation failures and error rates.
- Alert on spikes indicating potential attack or systemic issue.
- Correlate errors with user actions to detect misuse patterns.

---

## 10. Summary Checklist

- [ ] Fail-safe defaults implemented
- [ ] Input validation (schema & sanitization) applied
- [ ] Explicit opt-in for dangerous operations
- [ ] Structured error handling with logging
- [ ] Tests for misuse cases
- [ ] Least privilege enforced
- [ ] Graceful degradation paths defined

---

**End of Document**
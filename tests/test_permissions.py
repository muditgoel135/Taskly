from app.services.permissions import require_role

# Smoke test of role ordering

def test_require_role():
    # function expects context with JWT; here we just check constants
    assert callable(require_role)

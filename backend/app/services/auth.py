from functools import wraps

from flask import abort
from flask_login import current_user, login_required

# Role-Based Access Control (RBAC) Decorator
#
# In backend engineering, a decorator is a function that takes another function as an argument,
# extends its behavior without modifying it directly, and returns a new function.
#
# `role_required(*roles)` is a "decorator factory" that accepts a variable number of allowed roles
# (e.g. `@role_required('admin')` or `@role_required('admin', 'security_officer')`).
def role_required(*roles):
    def decorator(view_function):
        # `@wraps(view_function)` preserves the original function's name (`__name__`) and docstring (`__doc__`).
        # This is critical in Flask because Flask uses the function name as the internal endpoint name;
        # without `@wraps`, all decorated routes would share the same name ('wrapped_view') causing routing errors.
        @wraps(view_function)
        # `@login_required` ensures that only authenticated users reach this check.
        # If the user is anonymous, Flask-Login redirects them to the login page immediately.
        @login_required
        def wrapped_view(*args, **kwargs):
            # Authorization check: Ensure the authenticated user has one of the required roles.
            # If the user's role does not match, abort with HTTP 403 Forbidden.
            # (Note the difference: 401 Unauthorized means "you are not logged in",
            # whereas 403 Forbidden means "you are logged in, but you lack permission").
            if current_user.role not in roles:
                abort(403)

            # If the role check passes, execute the original view function and return its response.
            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator
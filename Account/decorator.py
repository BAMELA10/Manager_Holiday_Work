from django.http import HttpResponseForbidden
from functools import wraps

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == required_role:
                return view_func(request, *args, **kwargs)
            elif request.user.role in required_role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Unauthorized Access")
        return _wrapped_view
    return decorator
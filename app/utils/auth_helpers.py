from fastapi import Request
from fastapi.responses import RedirectResponse
from functools import wraps

def auth_required(route_func):
    @wraps(route_func)
    async def wrapper(request: Request, *args, **kwargs):
        if not request.session.get("user"):
            return RedirectResponse("/login", status_code=302)
        return await route_func(request, *args, **kwargs)
    return wrapper

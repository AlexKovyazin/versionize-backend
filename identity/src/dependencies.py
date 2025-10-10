from functools import wraps
from typing import List

from fastapi import Depends, HTTPException

from identity.src.domain.user import AuthenticatedUser
from identity.src.service.auth import keycloak_openid
from identity.src.service.auth import oauth2_scheme


async def get_authenticated_user(token: str = Depends(oauth2_scheme)) -> AuthenticatedUser:
    """
    Dependency to get current user from Keycloak token
    """
    try:
        token_info = await keycloak_openid.a_introspect(token)
        sub = token_info["sub"]

        if not sub:
            raise HTTPException(
                status_code=401,
                detail="User does not exists"
            )
        if not token_info.get("active"):
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        realm_access = token_info.get("realm_access", {})
        roles = realm_access.get("roles", [])

        return AuthenticatedUser(
            id=sub,
            roles=roles
        )

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}"
        )


def require_roles(required_roles: List[str]):
    """
    Decorator to require specific roles
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(
                *args,
                user: AuthenticatedUser = Depends(get_authenticated_user),
                **kwargs
        ):
            user_roles = set(user.roles)
            required_roles_set = set(required_roles)

            if not user_roles.intersection(required_roles_set):
                raise HTTPException(
                    status_code=403,
                    detail=f"Required roles: {required_roles}"
                )
            return await func(*args, current_user=user, **kwargs)

        return wrapper

    return decorator

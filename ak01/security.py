from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SecurityContext:
    actor_id: str
    namespace: str
    permissions: set[str] = field(default_factory=set)


class AuthorizationError(PermissionError):
    pass


def require_permission(ctx: SecurityContext, permission: str) -> None:
    if permission not in ctx.permissions:
        raise AuthorizationError(f"Missing permission: {permission}")


def enforce_namespace(ctx: SecurityContext, resource_namespace: str) -> None:
    if ctx.namespace != resource_namespace and "namespace:cross_read" not in ctx.permissions:
        raise AuthorizationError("Cross-namespace access denied")


def may_qualify(ctx: SecurityContext) -> bool:
    return "knowledge:qualify" in ctx.permissions and ctx.actor_id != "AK-01"

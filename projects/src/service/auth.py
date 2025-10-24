from fastapi.security import OAuth2AuthorizationCodeBearer

from projects.src.config.settings import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.kc_auth_url,
    tokenUrl=settings.kc_token_url,
    scopes={
        "openid": "OpenID Connect",
    }
)

from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

from identity.src.config.settings import settings

keycloak_openid = KeycloakOpenID(
    server_url=settings.kc_internal_base_url,
    client_id=settings.kc_client_id,
    realm_name=settings.kc_realm,
    client_secret_key=settings.kc_client_secret.get_secret_value(),
    verify=False if settings.debug else True,
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.kc_auth_url,
    tokenUrl=settings.kc_token_url,
    scopes={
        "openid": "OpenID Connect",
    }
)

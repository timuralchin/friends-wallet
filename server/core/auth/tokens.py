from rest_framework_simplejwt.tokens import AccessToken, BlacklistMixin


class JWTAccessToken(BlacklistMixin, AccessToken):
    """Custom black-listable access token."""
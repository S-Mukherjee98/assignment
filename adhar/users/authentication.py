# yourapp/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class VersionedJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        
        token_version = validated_token.get("token_version")
        if token_version != user.token_version:
            raise AuthenticationFailed("Access token is no longer valid.")

        return user

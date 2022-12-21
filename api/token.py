from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return smart_bytes(f"{user.pk}{timestamp}{user.is_verified}")


account_activation_token = TokenGenerator()
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


# create a token for sending to user for  confirm his/her registration
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) +
                text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()

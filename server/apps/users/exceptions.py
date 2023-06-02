from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

from server.core.exceptions import BaseCoreException


class UserExist(APIException):
    """User with provided email/username already joined."""

    status_code = 409
    default_detail = 'User with this email or username elready exist.'
    default_code = 'user_exist'


class UserAlreadyJoined(BaseCoreException):
    """Raises when user already joined with that username."""

    default_message = 'User already joined'


class ValidationError(BaseCoreException):
    """Validation error for fields."""

    default_message = 'Validation error'


class UserAlreadyHasRole(BaseCoreException):
    """Raises when user tries to add another role."""

    default_message = 'User already has role'


class SamePasswordError(BaseCoreException):
    """Raises when user tries to add another role."""

    default_message = """Your new password cannot be 
    the same as your current password"""


class PasswordValidationError(BaseCoreException):
    """Raises when user tries to add another role."""

    default_message = """Password must has at least 8 characters 
    that include at least 1 lowercase character, 1 uppercase character, 
    1 number and 1 special character in (!@#$%^&)"""


class ResetTokenInvalid(BaseCoreException):
    """Raise in password recovery process."""

    default_message = _('Reset token is invalid or expired')

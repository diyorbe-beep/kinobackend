"""
Custom exception handler with Telegram alerts.
"""
import logging
import traceback
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.conf import settings

from apps.shared.utils.custom_response import CustomResponse
from apps.shared.utils.telegram_alerts import alert_to_telegram


def custom_exception_handler(exc, context):
    """Custom exception handler that sends alerts to Telegram."""
    response = exception_handler(exc, context)
    
    request = context.get('request')

    logger = logging.getLogger(__name__)
    logger.error(f"Exception: {str(exc)}", exc_info=True)

    # Send Telegram alert only in production (not in DEBUG mode)
    if not getattr(settings, 'DEBUG', False):
        try:
            alert_to_telegram(
                traceback_text=traceback.format_exc(),
                message=str(exc),
                request=request
            )
        except Exception as alert_error:
            logger.error(f"Failed to send Telegram alert: {str(alert_error)}")

    # Handle validation errors
    if isinstance(exc, (DjangoValidationError, DRFValidationError)):
        errors = {}
        if hasattr(exc, 'detail'):
            errors = exc.detail
        elif hasattr(exc, 'message_dict'):
            errors = exc.message_dict
        else:
            errors = {'non_field_errors': [str(exc)]}
        
        return CustomResponse.validation_error(
            errors=errors,
            request=request,
            message_key="VALIDATION_ERROR"
        )

    # Handle specific HTTP status codes
    if response is not None:
        status_code = response.status_code
        
        if status_code == 401:
            return CustomResponse.unauthorized(
                request=request,
                message_key="UNAUTHORIZED"
            )
        elif status_code == 403:
            return CustomResponse.forbidden(
                request=request,
                message_key="PERMISSION_DENIED"
            )
        elif status_code == 404:
            return CustomResponse.not_found(
                request=request,
                message_key="NOT_FOUND"
            )
        elif status_code >= 500:
            return CustomResponse.internal_error(
                request=request,
                message_key="INTERNAL_SERVER_ERROR"
            )

    # Default to internal server error
    return CustomResponse.internal_error(
        request=request,
        message_key="INTERNAL_SERVER_ERROR"
    )





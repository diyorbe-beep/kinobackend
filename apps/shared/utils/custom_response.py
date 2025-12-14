"""
Custom response utilities for consistent API responses.
"""
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional, Union
from rest_framework.request import Request
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@dataclass
class ResponseBody:
    message_key: str
    request: Optional[Request] = None
    context: Optional[Dict[str, Any]] = None

    def get_language(self) -> str:
        """Get language from request."""
        if self.request and hasattr(self.request, 'lang'):
            return self.request.lang
        if self.request and hasattr(self.request, 'headers'):
            accept_lang = self.request.headers.get('Accept-Language', 'en')
            lang = accept_lang.split(';')[0].split(',')[0].strip()
            return lang
        return 'en'

    def to_dict(self, **kwargs) -> Dict[str, Any]:
        """Convert to dictionary."""
        lang = self.get_language()
        message = self._get_message(self.message_key, lang)
        response_body = {
            "id": message.get("id", "SUCCESS"),
            "message": message.get("message", "Success"),
            **kwargs
        }
        return response_body

    def get_status_code(self) -> int:
        """Get status code for message."""
        lang = self.get_language()
        message = self._get_message(self.message_key, lang)
        return message.get("status_code", 200)

    def _get_message(self, key: str, lang: str) -> Dict[str, Any]:
        """Get message detail."""
        messages = {
            "SUCCESS_MESSAGE": {"id": "SUCCESS", "message": "Success", "status_code": 200},
            "NOT_FOUND": {"id": "NOT_FOUND", "message": "Not found", "status_code": 404},
            "UNAUTHORIZED": {"id": "UNAUTHORIZED", "message": "Unauthorized", "status_code": 401},
            "PERMISSION_DENIED": {"id": "PERMISSION_DENIED", "message": "Permission denied", "status_code": 403},
            "VALIDATION_ERROR": {"id": "VALIDATION_ERROR", "message": "Validation error", "status_code": 400},
            "INTERNAL_SERVER_ERROR": {"id": "INTERNAL_SERVER_ERROR", "message": "Internal server error", "status_code": 500},
        }
        return messages.get(key, messages["SUCCESS_MESSAGE"])


class CustomResponse:
    """Custom response class for consistent API responses."""

    @staticmethod
    def success(
            message_key: str = "SUCCESS_MESSAGE",
            request: Request = None,
            data: Any = None,
            context: Dict[str, Any] = None,
            status_code: int = None,
            **kwargs
    ) -> Response:
        """Create success response."""
        body_maker = ResponseBody(
            message_key=message_key,
            request=request,
            context=context
        )
        body = body_maker.to_dict(data=data, **kwargs)
        final_status = status_code or body_maker.get_status_code()
        return Response(body, status=final_status)

    @staticmethod
    def error(
            message_key: str,
            request: Request = None,
            context: Dict[str, Any] = None,
            errors: Union[Dict[str, Any], str, Exception] = None,
            status_code: int = None,
            **kwargs
    ) -> Response:
        """Create error response."""
        body_maker = ResponseBody(
            message_key=message_key,
            request=request,
            context=context
        )
        response_data = {}
        if errors:
            response_data['errors'] = errors
        body = body_maker.to_dict(**response_data, **kwargs)
        final_status = status_code or body_maker.get_status_code()
        logger.warning(
            f"Error response: {message_key} (status: {final_status})",
            extra={'errors': errors, 'context': context}
        )
        return Response(body, status=final_status)

    @staticmethod
    def validation_error(
            errors: Dict[str, Any],
            request: Request = None,
            message_key: str = "VALIDATION_ERROR",
            context: Dict[str, Any] = None,
            **kwargs
    ) -> Response:
        """Create validation error response."""
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            errors=errors,
            status_code=400,
            **kwargs
        )

    @staticmethod
    def not_found(
            message_key: str = "NOT_FOUND",
            request: Request = None,
            context: Dict[str, Any] = None,
            **kwargs
    ) -> Response:
        """Create not found response."""
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            status_code=404,
            **kwargs
        )

    @staticmethod
    def unauthorized(
            message_key: str = "UNAUTHORIZED",
            request: Request = None,
            context: Dict[str, Any] = None,
            **kwargs
    ) -> Response:
        """Create unauthorized response."""
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            status_code=401,
            **kwargs
        )

    @staticmethod
    def forbidden(
            message_key: str = "PERMISSION_DENIED",
            request: Request = None,
            context: Dict[str, Any] = None,
            **kwargs
    ) -> Response:
        """Create forbidden response."""
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            status_code=403,
            **kwargs
        )





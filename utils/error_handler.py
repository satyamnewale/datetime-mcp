
import logging
from functools import wraps

from pydantic import ValidationError


logger = logging.getLogger(__name__)


def _format_validation_error(exc: ValidationError) -> str:
    """Convert Pydantic errors into concise, user-friendly messages."""

    messages = []

    for error in exc.errors(
        include_url=False,
        include_input=False,
    ):
        field = ".".join(str(item) for item in error["loc"])
        message = error["msg"]

        messages.append(f"{field}: {message}")

    return "Invalid input: " + "; ".join(messages)


def handle_tool_errors(func):
    """
    Centralized error handling for MCP tool functions.

    Expected errors:
        - Pydantic ValidationError
        - ValueError

    Unexpected errors:
        - Logged internally
        - Replaced with a safe error message
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValidationError as exc:
            raise ValueError(
                _format_validation_error(exc)
            ) from None

        except ValueError as exc:
            raise ValueError(str(exc)) from None

        except Exception:
            logger.exception(
                "Unexpected error in MCP tool: %s",
                func.__name__,
            )

            raise RuntimeError(
                "An unexpected internal error occurred. "
                "Please try again later."
            ) from None

    return wrapper

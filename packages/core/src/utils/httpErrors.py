# @license
# Copyright 2025 Google LLC
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Optional

class HttpError(Exception):
    """Base class for HTTP-related errors."""
    def __init__(self, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.status = status

class ModelNotFoundError(HttpError):
    """Custom error for when a model is not found."""
    def __init__(self, message: str, code: Optional[int] = 404):
        super().__init__(message, status=code)
        self.name = 'ModelNotFoundError'

def get_error_status(error: Any) -> Optional[int]:
    """
    Extracts the HTTP status code from an error object.

    Args:
        error: The error object.

    Returns:
        The HTTP status code, or None if not found.
    """
    # Check for a 'status' attribute on the error itself
    if hasattr(error, 'status') and isinstance(getattr(error, 'status'), int):
        return getattr(error, 'status')
    
    # Check for error.response.status (common in requests/aiohttp/axios like errors)
    if hasattr(error, 'response'):
        response = getattr(error, 'response')
        if hasattr(response, 'status') and isinstance(getattr(response, 'status'), int):
            return getattr(response, 'status')
            
    return None
from quart import jsonify

from src.app.exceptions import ServiceException


async def handle_service_exception(error: ServiceException):
    return jsonify({"detail": error.detail}), error.code


def get_exception_handlers():
    return {
        ServiceException: handle_service_exception,
    }

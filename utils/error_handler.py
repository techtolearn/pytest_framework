from enum import Enum


class ErrorType(Enum):
    ENV_ERROR = 1
    EMPTY_URL_ERROR = 2
    UNSUPPORTED_DRIVER_TYPE = 3


class ErrorHandler:
    DEFAULT_ERROR_MESSAGES = {
        ErrorType.ENV_ERROR: "Unsupported environment",
        ErrorType.EMPTY_URL_ERROR: "Environment variable is empty or not found",
        ErrorType.UNSUPPORTED_DRIVER_TYPE: "Unsupported driver type"
    }

    @staticmethod
    def raise_error(error_type, *args, custom_message=None):
        default_message = ErrorHandler.DEFAULT_ERROR_MESSAGES.get(error_type)
        args_str = " ".join(args) if args else ""
        message_parts = [default_message, args_str, custom_message]
        error_message = " ".join(filter(None, message_parts))
        raise ValueError(error_message)

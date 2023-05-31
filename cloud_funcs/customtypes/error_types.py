from enum import Enum

class CustomHttpErrorCode(Enum):
    UNAUTHORIZED = "unauthorized"
    DATABASE_ERROR = "database_error"
    PROBLEM_NOT_SOLVED = "problem_not_solved"
    TEXT_NOT_RECOGNIZED = "text_not_recognized"
    NO_REQUESTS_AVAILABLE = "no_requests_available"
    SUBJECT_NOT_RECOGNIZED = "subject_not_recognized"
    SUBJECT_NOT_SUPPORTED = "subject_not_supported"

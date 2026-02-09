"""
Domain-level exceptions.

These represent violations of business rules inside the domain layer.
"""


class DomainError(Exception):
    """Base class for all domain errors."""

    pass


# --- Generic errors ---
class EmptyFieldError(DomainError):
    """Raised when a required field is empty."""

    pass


class InvalidLengthError(DomainError):
    """Raised when a field exceeds allowed length."""

    def __init__(
        self,
        field: str,
        min_length: int | None = None,
        max_length: int | None = None,
    ):
        if min_length is not None:
            super().__init__(f"{field} must be at least {min_length} characters long")
        elif max_length is not None:
            super().__init__(f"{field} exceeds maximum length of {max_length}")
        else:
            super().__init__(f"Invalid length for {field}")


class InvalidURLError(DomainError):
    """Raised when a URL is invalid."""

    pass


class InvalidDateRangeError(DomainError):
    """Raised when start_date > end_date."""

    pass


class InvalidOrderIndexError(DomainError):
    """Raised when order_index is invalid."""

    pass


# --- Name / Title / Description ---
class InvalidNameError(DomainError):
    """Raised when a name is invalid."""

    pass


class InvalidTitleError(DomainError):
    """Raised when a title is invalid."""

    pass


class InvalidDescriptionError(DomainError):
    """Raised when a description is invalid."""

    pass


# --- Category / Skill ---
class InvalidCategoryError(DomainError):
    """Raised when a category is invalid."""

    pass


class InvalidSkillLevelError(DomainError):
    """Raised when a skill level is invalid."""

    pass


# --- WorkExperience-specific ---
class InvalidRoleError(DomainError):
    """Raised when a role is invalid."""

    pass


class InvalidCompanyError(DomainError):
    """Raised when a company name is invalid."""

    pass


# --- Certification-specific ---
class InvalidIssuerError(DomainError):
    """Raised when the issuer is invalid."""

    pass


# --- Education-specific ---
class InvalidInstitutionError(DomainError):
    """Raised when the institution name is invalid."""

    pass


# --- Contact / Social ---
class InvalidEmailError(DomainError):
    """Raised when an email is invalid."""

    pass


class InvalidPhoneError(DomainError):
    """Raised when a phone number is invalid."""

    pass


# --- Project / Platform ---
class InvalidPlatformError(DomainError):
    """Raised when a platform name is invalid."""

    pass


# --- AdditionalTraining-specific ---
class InvalidProviderError(DomainError):
    """Raised when the provider is invalid."""

    pass


class DuplicateValueError(DomainError):
    """Raised when a unique constraint is violated."""

    pass


# --- ProgrammingLanguage-specific ---
class InvalidProgrammingLanguageLevelError(DomainError):
    """Raised when a programming language level is invalid."""

    pass


# --- Language-specific ---
class InvalidLanguageProficiencyError(DomainError):
    """Raised when a language proficiency level is invalid."""

    pass

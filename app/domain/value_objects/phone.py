"""
Phone Value Object.

Represents a validated phone number following E.164 international format.

Value Object Principles:
- Immutability: Cannot be changed after creation
- Self-validation: Validates format on construction
- Equality by value: Two Phones are equal if numbers match
"""

from dataclasses import dataclass
import re

from app.domain.exceptions import EmptyFieldError, InvalidPhoneError


@dataclass(frozen=True)
class Phone:
    """
    Phone Value Object representing a validated phone number.

    Attributes:
        value: The phone number string (stored normalized)

    Business Rules:
        - Must be non-empty
        - Must follow E.164 format (international)
        - Can contain spaces, dashes, parentheses (removed on normalization)
        - Stored in normalized format

    Examples:
        - '+34612345678'
        - '+1-555-123-4567'
        - '+44 20 7123 4567'
    """

    value: str

    # E.164 pattern: + followed by 1-15 digits
    E164_PATTERN = re.compile(r"^\+?[1-9]\d{1,14}$")

    # Pattern to extract digits from formatted numbers
    DIGIT_PATTERN = re.compile(r"[\d+]+")

    def __post_init__(self):
        original = self.value
        normalized = self._normalize(original)
        object.__setattr__(self, "value", normalized)
        self._validate(original)

    @staticmethod
    def create(value: str) -> "Phone":
        """
        Factory method to create a Phone.

        Args:
            value: Phone number string (can be formatted)

        Returns:
            A new Phone instance

        Raises:
            EmptyFieldError: If value is empty
            InvalidPhoneError: If format is invalid
        """
        return Phone(value=value)

    @staticmethod
    def try_create(value: str) -> "Phone | None":
        """
        Try to create a Phone, returning None if invalid.

        Args:
            value: Phone number string

        Returns:
            Phone instance or None if invalid
        """
        try:
            return Phone.create(value)
        except (InvalidPhoneError, EmptyFieldError):
            return None

    @staticmethod
    def from_e164(value: str) -> "Phone":
        """
        Create a Phone from E.164 format directly.

        Args:
            value: Phone in E.164 format (e.g., '+34612345678')

        Returns:
            A new Phone instance
        """
        return Phone(value=value)

    def get_country_code(self) -> str:
        """
        Extract country code from phone number.

        Returns:
            Country code (1-3 digits after +)

        Note:
            This is a simple extraction. For proper country code detection,
            use a library like phonenumbers.
        """
        # Simple heuristic: country codes are 1-3 digits
        digits = self.value[1:] if self.value.startswith("+") else self.value

        # Try to extract country code (1-3 digits)
        if len(digits) >= 10:
            # Most likely format: +CC XXXXXXXXX (CC = 1-3 digits)
            for length in [3, 2, 1]:
                potential_code = digits[:length]
                if potential_code.isdigit():
                    return potential_code

        return digits[:2]  # Fallback

    def get_national_number(self) -> str:
        """
        Get the national number (without country code).

        Returns:
            National number portion
        """
        country_code = self.get_country_code()
        if self.value.startswith("+"):
            return self.value[1 + len(country_code) :]
        return self.value

    def format_international(self) -> str:
        """
        Format phone number in international style.

        Returns:
            Formatted phone (e.g., '+34 612 345 678')
        """
        if not self.value.startswith("+"):
            return self.value

        # Simple formatting: +CC NNN NNN NNN
        digits = self.value[1:]
        country_code = self.get_country_code()
        national = digits[len(country_code) :]

        # Format national number in groups of 3
        formatted_national = " ".join(
            [national[i : i + 3] for i in range(0, len(national), 3)]
        )

        return f"+{country_code} {formatted_national}"

    def _normalize(self, value: str) -> str:
        """
        Normalize phone number to E.164 format.

        Args:
            value: Raw phone number

        Returns:
            Normalized phone number
        """
        if not value:
            return value

        # Remove all non-digit characters except +
        normalized = "".join(c for c in value if c.isdigit() or c == "+")

        # Ensure it starts with +
        if not normalized.startswith("+"):
            # If no country code, we can't normalize properly
            # Keep as-is for validation to fail
            return normalized

        return normalized

    def _validate(self, original: str) -> None:
        # Caso 1: el usuario realmente envió vacío
        if original is None or original.strip() == "":
            raise EmptyFieldError("phone")

        # Caso 2: la normalización lo dejó vacío → inválido
        if self.value is None or self.value.strip() == "":
            raise InvalidPhoneError(f"Invalid phone number: {original}")

        # Caso 3: no empieza por + o no son dígitos
        if not self.value.startswith("+") or not self.value[1:].isdigit():
            raise InvalidPhoneError(f"Invalid phone number: {original}")

        # Caso 4: no cumple E.164
        if not self.E164_PATTERN.match(self.value):
            raise InvalidPhoneError(f"Invalid phone number: {original}")

    def __str__(self) -> str:
        """String representation for display (formatted)."""
        return self.format_international()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Phone('{self.value}')"

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, Phone):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.value)

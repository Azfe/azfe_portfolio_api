"""
Tool Entity.

Represents a tool, technology, or software used in the portfolio.

Business Rules Applied:
- RB-T01: name is required (1-50 chars)
- RB-T02: name must be unique per profile
- RB-T03: category is required (1-50 chars, e.g., "Framework", "Database")
- RB-T04: iconUrl is optional, must be valid URL if provided
- RB-T05: orderIndex is required for display ordering
"""

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import (
    EmptyFieldError,
    InvalidCategoryError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidURLError,
)


@dataclass
class Tool:
    """
    Tool entity representing a technology, framework, or software tool.

    This entity maintains uniqueness by name and validates icon URLs.
    """

    id: str
    profile_id: str
    name: str
    category: str
    order_index: int
    icon_url: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_NAME_LENGTH = 50
    MAX_CATEGORY_LENGTH = 50
    URL_PATTERN = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_profile_id()
        self._validate_name()
        self._validate_category()
        self._validate_icon_url()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        name: str,
        category: str,
        order_index: int,
        icon_url: str | None = None,
    ) -> "Tool":
        """
        Factory method to create a new Tool.

        Args:
            profile_id: Reference to the Profile
            name: Tool name (e.g., "Docker", "PostgreSQL")
            category: Tool category (e.g., "Container", "Database")
            order_index: Position in the ordered list
            icon_url: URL to tool icon/logo (optional)

        Returns:
            A new Tool instance with generated UUID
        """
        return Tool(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            name=name,
            category=category,
            order_index=order_index,
            icon_url=icon_url,
        )

    def update_info(
        self,
        name: str | None = None,
        category: str | None = None,
        icon_url: str | None = None,
    ) -> None:
        """
        Update tool information.

        Args:
            name: New name (optional)
            category: New category (optional)
            icon_url: New icon URL (optional)
        """
        if name is not None:
            self.name = name
            self._validate_name()

        if category is not None:
            self.category = category
            self._validate_category()

        if icon_url is not None:
            self.icon_url = icon_url
            self._validate_icon_url()

        self._mark_as_updated()

    def update_order(self, new_order_index: int) -> None:
        """
        Update the order index.

        Args:
            new_order_index: New position in the list
        """
        self.order_index = new_order_index
        self._validate_order_index()
        self._mark_as_updated()

    def remove_icon(self) -> None:
        """Remove the icon URL."""
        self.icon_url = None
        self._mark_as_updated()

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_name(self) -> None:
        """Validate name field according to business rules."""
        if not self.name or not self.name.strip():
            raise InvalidNameError("Tool name cannot be empty")

        if len(self.name) > self.MAX_NAME_LENGTH:
            raise InvalidLengthError("name", max_length=self.MAX_NAME_LENGTH)

    def _validate_category(self) -> None:
        """Validate category field according to business rules."""
        if not self.category or not self.category.strip():
            raise InvalidCategoryError("Category cannot be empty")

        if len(self.category) > self.MAX_CATEGORY_LENGTH:
            raise InvalidLengthError("category", max_length=self.MAX_CATEGORY_LENGTH)

    def _validate_icon_url(self) -> None:
        """Validate icon URL format if provided."""
        if self.icon_url is not None:
            if self.icon_url.strip() == "":
                self.icon_url = None
            elif not self.URL_PATTERN.match(self.icon_url):
                raise InvalidURLError(self.icon_url)

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Tool(id={self.id}, name={self.name}, category={self.category})"

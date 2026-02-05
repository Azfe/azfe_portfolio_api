"""
Project Entity.

Represents a professional project in the portfolio.

Business Rules Applied:
- RB-PR01: title is required (1-100 chars)
- RB-PR02: description is required (1-2000 chars)
- RB-PR03: startDate is required
- RB-PR04: endDate is optional (must be after startDate if provided)
- RB-PR05: liveUrl is optional, must be valid URL if provided
- RB-PR06: repoUrl is optional, must be valid URL if provided
- RB-PR07: technologies is optional array (max 20 items, each max 50 chars)
- RB-PR08: orderIndex is required and must be unique per profile
- RB-PR09: If no URLs, description must be sufficiently detailed (min 100 chars)
"""

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import (
    EmptyFieldError,
    InvalidDateRangeError,
    InvalidDescriptionError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidTitleError,
    InvalidURLError,
)


@dataclass
class Project:
    """
    Project entity representing a professional project.

    This entity maintains temporal coherence, URL validation, and ordering.
    """

    id: str
    profile_id: str
    title: str
    description: str
    start_date: datetime
    order_index: int
    end_date: datetime | None = None
    live_url: str | None = None
    repo_url: str | None = None
    technologies: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_TITLE_LENGTH = 100
    MIN_DESCRIPTION_LENGTH = 10
    MAX_DESCRIPTION_LENGTH = 2000
    MIN_DESCRIPTION_WITHOUT_URLS = 100
    MAX_TECHNOLOGIES = 20
    MAX_TECHNOLOGY_LENGTH = 50
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
        self._validate_title()
        self._validate_description()
        self._validate_dates()
        self._validate_urls()
        self._validate_technologies()
        self._validate_order_index()
        self._validate_description_sufficiency()

    @staticmethod
    def create(
        profile_id: str,
        title: str,
        description: str,
        start_date: datetime,
        order_index: int,
        end_date: datetime | None = None,
        live_url: str | None = None,
        repo_url: str | None = None,
        technologies: list[str] | None = None,
    ) -> "Project":
        """
        Factory method to create a new Project.

        Args:
            profile_id: Reference to the Profile
            title: Project title
            description: Project description
            start_date: When the project started
            order_index: Position in the ordered list
            end_date: When the project ended (None if ongoing)
            live_url: URL to live project
            repo_url: URL to repository
            technologies: List of technologies used

        Returns:
            A new Project instance with generated UUID
        """
        return Project(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            title=title,
            description=description,
            start_date=start_date,
            order_index=order_index,
            end_date=end_date,
            live_url=live_url,
            repo_url=repo_url,
            technologies=technologies or [],
        )

    def update_info(
        self,
        title: str | None = None,
        description: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> None:
        """
        Update project basic information.

        Args:
            title: New title (optional)
            description: New description (optional)
            start_date: New start date (optional)
            end_date: New end date (optional)
        """
        if title is not None:
            self.title = title
            self._validate_title()

        if description is not None:
            self.description = description
            self._validate_description()

        if start_date is not None:
            self.start_date = start_date

        if end_date is not None:
            self.end_date = end_date

        self._validate_dates()
        self._validate_description_sufficiency()
        self._mark_as_updated()

    def update_urls(
        self,
        live_url: str | None = None,
        repo_url: str | None = None,
    ) -> None:
        """
        Update project URLs.

        Args:
            live_url: New live URL (optional)
            repo_url: New repository URL (optional)
        """
        if live_url is not None:
            self.live_url = live_url

        if repo_url is not None:
            self.repo_url = repo_url

        self._validate_urls()
        self._validate_description_sufficiency()
        self._mark_as_updated()

    def update_technologies(self, technologies: list[str]) -> None:
        """
        Update technologies list.

        Args:
            technologies: New list of technologies
        """
        self.technologies = technologies
        self._validate_technologies()
        self._mark_as_updated()

    def add_technology(self, technology: str) -> None:
        """
        Add a single technology.

        Args:
            technology: Technology name to add
        """
        if len(self.technologies) >= self.MAX_TECHNOLOGIES:
            raise InvalidLengthError("technologies", max_length=self.MAX_TECHNOLOGIES)

        if not technology or not technology.strip():
            raise EmptyFieldError("technology")

        if len(technology) > self.MAX_TECHNOLOGY_LENGTH:
            raise InvalidLengthError(
                "technology", max_length=self.MAX_TECHNOLOGY_LENGTH
            )

        self.technologies.append(technology)
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

    def is_ongoing(self) -> bool:
        """Check if this project is ongoing (no end date)."""
        return self.end_date is None

    def has_urls(self) -> bool:
        """Check if project has any URLs."""
        return bool(self.live_url or self.repo_url)

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_title(self) -> None:
        """Validate title field according to business rules."""
        if not self.title or not self.title.strip():
            raise InvalidTitleError("Title cannot be empty")

        if len(self.title) > self.MAX_TITLE_LENGTH:
            raise InvalidLengthError("title", max_length=self.MAX_TITLE_LENGTH)

    def _validate_description(self) -> None:
        """Validate description field according to business rules."""
        if not self.description or not self.description.strip():
            raise InvalidDescriptionError("Description cannot be empty")

        if len(self.description) < self.MIN_DESCRIPTION_LENGTH:
            raise InvalidLengthError(
                "description", min_length=self.MIN_DESCRIPTION_LENGTH
            )

        if len(self.description) > self.MAX_DESCRIPTION_LENGTH:
            raise InvalidLengthError(
                "description", max_length=self.MAX_DESCRIPTION_LENGTH
            )

    def _validate_description_sufficiency(self) -> None:
        """
        Validate that description is sufficiently detailed if no URLs provided.
        Business rule: RB-PR09
        """
        if (
            not self.has_urls()
            and len(self.description) < self.MIN_DESCRIPTION_WITHOUT_URLS
        ):
            raise InvalidDescriptionError(
                f"Description must be at least {self.MIN_DESCRIPTION_WITHOUT_URLS} "
                f"characters when no URLs are provided"
            )

    def _validate_dates(self) -> None:
        """Validate date range coherence."""
        if self.end_date is not None and self.end_date <= self.start_date:
            raise InvalidDateRangeError(str(self.start_date), str(self.end_date))

    def _validate_urls(self) -> None:
        """Validate URL formats."""
        if self.live_url is not None:
            if self.live_url.strip() == "":
                self.live_url = None
            elif not self.URL_PATTERN.match(self.live_url):
                raise InvalidURLError(self.live_url)

        if self.repo_url is not None:
            if self.repo_url.strip() == "":
                self.repo_url = None
            elif not self.URL_PATTERN.match(self.repo_url):
                raise InvalidURLError(self.repo_url)

    def _validate_technologies(self) -> None:
        """Validate technologies list."""
        if len(self.technologies) > self.MAX_TECHNOLOGIES:
            raise InvalidLengthError("technologies", max_length=self.MAX_TECHNOLOGIES)

        for tech in self.technologies:
            if not tech or not tech.strip():
                raise EmptyFieldError("technology item")
            if len(tech) > self.MAX_TECHNOLOGY_LENGTH:
                raise InvalidLengthError(
                    "technology item", max_length=self.MAX_TECHNOLOGY_LENGTH
                )

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Project(id={self.id}, title={self.title})"

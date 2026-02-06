"""
Mapper Interface.

This module defines the mapper interface for converting between different
representations of data across architectural layers.

Mappers translate between:
- Domain entities ↔ Persistence models (MongoDB documents)
- Domain entities ↔ DTOs (API request/response)
- DTOs ↔ Persistence models (in some cases)

Key Principles:
- Separation of Concerns: Each layer has its own representation
- Explicit Conversion: No automatic mapping, always explicit
- Bidirectional: Can convert in both directions
- Type Safety: Strongly typed conversions
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Generic types for domain and persistence models
TDomain = TypeVar("TDomain")
TPersistence = TypeVar("TPersistence")


class IMapper(ABC, Generic[TDomain, TPersistence]):
    """
    Generic Mapper Interface.

    Defines the contract for converting between domain entities and
    persistence models (or other representations).

    Type Parameters:
        TDomain: The domain entity type
        TPersistence: The persistence model type (e.g., MongoDB document dict)

    Design Patterns:
        - Data Mapper Pattern: Separates domain logic from persistence
        - Adapter Pattern: Adapts between different representations

    Usage:
        class ProfileMapper(IMapper[Profile, Dict[str, Any]]):
            def to_domain(self, persistence_model: Dict[str, Any]) -> Profile:
                return Profile(
                    id=str(persistence_model['_id']),
                    name=persistence_model['name'],
                    # ... more fields
                )

            def to_persistence(self, domain_entity: Profile) -> Dict[str, Any]:
                return {
                    '_id': ObjectId(domain_entity.id),
                    'name': domain_entity.name,
                    # ... more fields
                }

    Notes:
        - Mappers belong in the infrastructure layer
        - Mappers know about both domain and persistence representations
        - Mappers should handle type conversions (e.g., UUID ↔ ObjectId)
        - Mappers should handle nested objects and collections
    """

    @abstractmethod
    def to_domain(self, persistence_model: TPersistence) -> TDomain:
        """
        Convert from persistence model to domain entity.

        Args:
            persistence_model: The persistence representation

        Returns:
            The domain entity

        Notes:
            - Should reconstruct full domain entity
            - Should handle type conversions
            - Should validate data integrity
            - May raise exceptions for invalid data

        Examples:
            profile = mapper.to_domain(mongo_document)
        """
        pass

    @abstractmethod
    def to_persistence(self, domain_entity: TDomain) -> TPersistence:
        """
        Convert from domain entity to persistence model.

        Args:
            domain_entity: The domain entity

        Returns:
            The persistence representation

        Notes:
            - Should extract all necessary fields
            - Should handle type conversions
            - Should prepare data for storage
            - Should not include computed fields

        Examples:
            mongo_document = mapper.to_persistence(profile)
        """
        pass

    def to_domain_list(self, persistence_models: list[TPersistence]) -> list[TDomain]:
        """
        Convert a list of persistence models to domain entities.

        Args:
            persistence_models: List of persistence representations

        Returns:
            List of domain entities

        Notes:
            - Default implementation maps each item
            - Can be overridden for optimization
        """
        return [self.to_domain(model) for model in persistence_models]

    def to_persistence_list(self, domain_entities: list[TDomain]) -> list[TPersistence]:
        """
        Convert a list of domain entities to persistence models.

        Args:
            domain_entities: List of domain entities

        Returns:
            List of persistence representations

        Notes:
            - Default implementation maps each item
            - Can be overridden for optimization
        """
        return [self.to_persistence(entity) for entity in domain_entities]


class IDTOMapper(ABC, Generic[TDomain, TPersistence]):
    """
    DTO Mapper Interface.

    Specialized mapper for converting between domain entities and DTOs
    (Data Transfer Objects) used in the API layer.

    Type Parameters:
        TDomain: The domain entity type
        TPersistence: The DTO type (usually Pydantic model)

    Usage:
        class ProfileDTOMapper(IDTOMapper[Profile, ProfileDTO]):
            def to_dto(self, domain_entity: Profile) -> ProfileDTO:
                return ProfileDTO(
                    id=domain_entity.id,
                    name=domain_entity.name,
                    # ... more fields
                )

            def to_domain(self, dto: ProfileDTO) -> Profile:
                return Profile(
                    id=dto.id,
                    name=dto.name,
                    # ... more fields
                )

    Notes:
        - DTOs are typically Pydantic models in FastAPI
        - DTOs may have different structure than domain entities
        - DTOs may flatten nested objects
        - DTOs may include computed/derived fields
    """

    @abstractmethod
    def to_dto(self, domain_entity: TDomain) -> TPersistence:
        """
        Convert from domain entity to DTO.

        Args:
            domain_entity: The domain entity

        Returns:
            The DTO representation

        Notes:
            - Should include all fields needed by API consumers
            - May include computed fields
            - May flatten nested structures
            - Should handle null/optional fields
        """
        pass

    @abstractmethod
    def from_dto(self, dto: TPersistence) -> TDomain:
        """
        Convert from DTO to domain entity.

        Args:
            dto: The DTO

        Returns:
            The domain entity

        Notes:
            - Should validate business rules
            - Should reconstruct nested objects
            - May need to fetch related entities
            - Should handle default values
        """
        pass

    def to_dto_list(self, domain_entities: list[TDomain]) -> list[TPersistence]:
        """Convert a list of domain entities to DTOs."""
        return [self.to_dto(entity) for entity in domain_entities]

    def from_dto_list(self, dtos: list[TPersistence]) -> list[TDomain]:
        """Convert a list of DTOs to domain entities."""
        return [self.from_dto(dto) for dto in dtos]


class IValueObjectMapper(ABC, Generic[TDomain, TPersistence]):
    """
    Value Object Mapper Interface.

    Specialized mapper for converting value objects between representations.

    Type Parameters:
        TDomain: The value object type
        TPersistence: The primitive/dict representation

    Usage:
        class EmailMapper(IValueObjectMapper[Email, str]):
            def to_primitive(self, value_object: Email) -> str:
                return value_object.value

            def from_primitive(self, primitive: str) -> Email:
                return Email.create(primitive)

    Notes:
        - Value objects often map to primitives (str, int, dict)
        - Value objects validate on construction
        - Mappers should handle validation errors
    """

    @abstractmethod
    def to_primitive(self, value_object: TDomain) -> TPersistence:
        """
        Convert value object to primitive representation.

        Args:
            value_object: The value object

        Returns:
            Primitive representation (str, int, dict, etc.)
        """
        pass

    @abstractmethod
    def from_primitive(self, primitive: TPersistence) -> TDomain:
        """
        Convert primitive to value object.

        Args:
            primitive: Primitive representation

        Returns:
            The value object

        Raises:
            ValidationError: If primitive is invalid
        """
        pass

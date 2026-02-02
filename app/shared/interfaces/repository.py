"""
Repository Interface (Port).

This module defines the generic repository interface following the Repository Pattern
and Ports & Adapters architecture (Hexagonal Architecture).

The repository interface acts as a PORT that defines the contract for data access,
while concrete implementations (in infrastructure layer) act as ADAPTERS.

Key Principles:
- Domain layer defines the interface (Port)
- Infrastructure layer implements the interface (Adapter)
- Use cases depend on the interface, not the implementation
- Enables testability through dependency inversion
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any, TYPE_CHECKING

# Import entities only for type checking to avoid circular imports
if TYPE_CHECKING:
    from app.domain.entities import (
        Profile,
        WorkExperience,
        Skill,
        Education,
        Project,
        Certification,
        AdditionalTraining,
        ContactInformation,
        ContactMessage,
        SocialNetwork,
        Tool,
    )

# Generic type representing any domain entity
T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """
    Generic Repository Interface defining the contract for data persistence.
    
    This interface abstracts away data storage details, allowing the domain
    and application layers to remain independent of infrastructure choices.
    
    Type Parameters:
        T: The domain entity type this repository manages
        
    Design Patterns:
        - Repository Pattern: Mediates between domain and data mapping layers
        - Dependency Inversion: High-level modules depend on abstractions
        - Interface Segregation: Minimal, focused contract
        
    Usage:
        class ProfileRepository(IRepository[Profile]):
            async def add(self, entity: Profile) -> Profile:
                # MongoDB implementation
                ...
                
    Notes:
        - All methods are async to support async database drivers (Motor for MongoDB)
        - Methods should raise domain exceptions on failure
        - Implementations handle mapping between domain entities and persistence models
    """

    @abstractmethod
    async def add(self, entity: T) -> T:
        """
        Add a new entity to the repository.
        
        Args:
            entity: The domain entity to persist
            
        Returns:
            The persisted entity (may include generated fields like timestamps)
            
        Raises:
            DuplicateValueError: If entity with same unique constraint already exists
            DomainError: For other business rule violations
            
        Notes:
            - Should validate entity before persisting
            - Should handle ID generation if needed
            - Should set created_at/updated_at timestamps
            - Should return the persisted entity with all generated fields
        """
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """
        Update an existing entity in the repository.
        
        Args:
            entity: The domain entity with updated values
            
        Returns:
            The updated entity
            
        Raises:
            NotFoundException: If entity with given ID doesn't exist
            DomainError: For business rule violations
            
        Notes:
            - Should validate entity before persisting
            - Should update updated_at timestamp
            - Should return the updated entity
            - ID cannot be changed
        """
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """
        Delete an entity from the repository.
        
        Args:
            entity_id: The unique identifier of the entity to delete
            
        Returns:
            True if entity was deleted, False if not found
            
        Notes:
            - Should be idempotent (deleting non-existent entity returns False)
            - Should handle cascade deletes if needed
            - Consider soft deletes for audit trails
        """
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Retrieve an entity by its unique identifier.
        
        Args:
            entity_id: The unique identifier of the entity
            
        Returns:
            The entity if found, None otherwise
            
        Notes:
            - Should return None instead of raising exception if not found
            - Should reconstruct full domain entity from persistence model
        """
        pass

    @abstractmethod
    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        ascending: bool = True
    ) -> List[T]:
        """
        List all entities with optional pagination and sorting.
        
        Args:
            skip: Number of entities to skip (for pagination)
            limit: Maximum number of entities to return
            sort_by: Field name to sort by (optional)
            ascending: Sort direction (True for ascending, False for descending)
            
        Returns:
            List of entities (may be empty)
            
        Notes:
            - Should support pagination for large datasets
            - Should support sorting by any entity field
            - Should return empty list if no entities exist
            - Default limit prevents overwhelming responses
        """
        pass

    @abstractmethod
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count entities matching optional filters.
        
        Args:
            filters: Optional dictionary of field:value filters
            
        Returns:
            Number of entities matching filters
            
        Notes:
            - Should support common filter operations
            - Should return 0 if no entities match
            - Useful for pagination metadata
        """
        pass

    @abstractmethod
    async def exists(self, entity_id: str) -> bool:
        """
        Check if an entity exists by its unique identifier.
        
        Args:
            entity_id: The unique identifier of the entity
            
        Returns:
            True if entity exists, False otherwise
            
        Notes:
            - Should be more efficient than get_by_id when only existence matters
            - Useful for validation logic
        """
        pass

    @abstractmethod
    async def find_by(self, **filters) -> List[T]:
        """
        Find entities matching specified filters.
        
        Args:
            **filters: Arbitrary keyword arguments representing field:value filters
            
        Returns:
            List of entities matching all filters (may be empty)
            
        Examples:
            # Find by single field
            profiles = await repo.find_by(name="John Doe")
            
            # Find by multiple fields
            skills = await repo.find_by(category="Programming", level="expert")
            
        Notes:
            - Should support equality filters on any entity field
            - Should return empty list if no entities match
            - Implementations may support more complex query operations
        """
        pass


class IProfileRepository(IRepository['Profile']):
    """
    Profile-specific repository interface.
    
    Extends the generic repository with profile-specific queries.
    Only ONE profile should exist in the system.
    """

    @abstractmethod
    async def get_profile(self) -> Optional['Profile']:
        """
        Get the single profile (only one should exist).
        
        Returns:
            The profile if it exists, None otherwise
            
        Business Rule:
            Only one profile can exist in the system
        """
        pass

    @abstractmethod
    async def profile_exists(self) -> bool:
        """
        Check if a profile already exists.
        
        Returns:
            True if profile exists, False otherwise
            
        Business Rule:
            Used to enforce single profile constraint
        """
        pass


class IOrderedRepository(IRepository[T], Generic[T]):
    """
    Repository interface for entities with ordering (orderIndex).
    
    Adds methods to manage entity ordering.
    """

    @abstractmethod
    async def get_by_order_index(self, profile_id: str, order_index: int) -> Optional[T]:
        """
        Get entity by its order index within a profile.
        
        Args:
            profile_id: The profile ID
            order_index: The order index
            
        Returns:
            The entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all_ordered(
        self,
        profile_id: str,
        ascending: bool = True
    ) -> List[T]:
        """
        Get all entities for a profile, sorted by orderIndex.
        
        Args:
            profile_id: The profile ID
            ascending: Sort direction
            
        Returns:
            List of entities sorted by orderIndex
        """
        pass

    @abstractmethod
    async def reorder(
        self,
        profile_id: str,
        entity_id: str,
        new_order_index: int
    ) -> None:
        """
        Reorder an entity and adjust other entities' orderIndex accordingly.
        
        Args:
            profile_id: The profile ID
            entity_id: The entity to reorder
            new_order_index: The new order index
            
        Notes:
            - Should adjust other entities to maintain unique orderIndex
            - Should handle gaps in ordering
        """
        pass


class IContactMessageRepository(IRepository['ContactMessage']):
    """
    ContactMessage-specific repository interface.
    
    Extends the generic repository with message-specific queries.
    """

    @abstractmethod
    async def get_pending_messages(self) -> List['ContactMessage']:
        """
        Get all pending contact messages.
        
        Returns:
            List of messages with status='pending'
        """
        pass

    @abstractmethod
    async def get_messages_by_status(self, status: str) -> List['ContactMessage']:
        """
        Get messages filtered by status.
        
        Args:
            status: Message status (pending, read, replied)
            
        Returns:
            List of messages with specified status
        """
        pass

    @abstractmethod
    async def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a message as read.
        
        Args:
            message_id: The message ID
            
        Returns:
            True if updated, False if not found
        """
        pass

    @abstractmethod
    async def mark_as_replied(self, message_id: str) -> bool:
        """
        Mark a message as replied.
        
        Args:
            message_id: The message ID
            
        Returns:
            True if updated, False if not found
        """
        pass


class IUniqueNameRepository(IRepository[T], Generic[T]):
    """
    Repository interface for entities with unique names per profile.
    
    Used for Skill and Tool entities.
    """

    @abstractmethod
    async def exists_by_name(self, profile_id: str, name: str) -> bool:
        """
        Check if an entity with the given name exists for the profile.
        
        Args:
            profile_id: The profile ID
            name: The name to check
            
        Returns:
            True if exists, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_name(self, profile_id: str, name: str) -> Optional[T]:
        """
        Get entity by name within a profile.
        
        Args:
            profile_id: The profile ID
            name: The name to search for
            
        Returns:
            The entity if found, None otherwise
        """
        pass


class ISocialNetworkRepository(IRepository['SocialNetwork']):
    """
    SocialNetwork-specific repository interface.
    
    Extends the generic repository with social network-specific queries.
    """

    @abstractmethod
    async def exists_by_platform(self, profile_id: str, platform: str) -> bool:
        """
        Check if a social network with the given platform exists.
        
        Args:
            profile_id: The profile ID
            platform: The platform name (e.g., "LinkedIn", "GitHub")
            
        Returns:
            True if exists, False otherwise
            
        Business Rule:
            Only one social network per platform per profile
        """
        pass

    @abstractmethod
    async def get_by_platform(self, profile_id: str, platform: str) -> Optional['SocialNetwork']:
        """
        Get social network by platform within a profile.
        
        Args:
            profile_id: The profile ID
            platform: The platform name
            
        Returns:
            The social network if found, None otherwise
        """
        pass


# Type aliases for convenience
# Using string literals to avoid circular imports at runtime
ProfileRepository = IProfileRepository
WorkExperienceRepository = IOrderedRepository['WorkExperience']
SkillRepository = IUniqueNameRepository['Skill']
EducationRepository = IOrderedRepository['Education']
ProjectRepository = IOrderedRepository['Project']
CertificationRepository = IOrderedRepository['Certification']
AdditionalTrainingRepository = IOrderedRepository['AdditionalTraining']
ContactInformationRepository = IRepository['ContactInformation']
ContactMessageRepository = IContactMessageRepository
SocialNetworkRepository = ISocialNetworkRepository
ToolRepository = IUniqueNameRepository['Tool']
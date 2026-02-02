"""
Use Case Interface.

This module defines the generic use case interface following Clean Architecture
and the Command/Query pattern.

Use cases represent the application's business logic and orchestrate the flow
of data between entities and external interfaces (repositories, services).

Key Principles:
- Single Responsibility: Each use case does one thing
- Dependency Inversion: Depends on repository interfaces, not implementations
- Testability: Easy to mock dependencies
- Clear contract: Request -> Use Case -> Response
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Generic types for request and response
TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse')


class IUseCase(ABC, Generic[TRequest, TResponse]):
    """
    Generic Use Case Interface.
    
    Defines the contract for all use cases in the application.
    Each use case encapsulates a single business operation.
    
    Type Parameters:
        TRequest: The input type (DTO, command, query)
        TResponse: The output type (DTO, result, data)
        
    Design Patterns:
        - Command Pattern: Encapsulates a request as an object
        - Single Responsibility: Each use case does one thing
        - Interface Segregation: Minimal contract
        
    Usage:
        class GetProfileUseCase(IUseCase[GetProfileRequest, GetProfileResponse]):
            def __init__(self, profile_repo: IProfileRepository):
                self.profile_repo = profile_repo
                
            async def execute(self, request: GetProfileRequest) -> GetProfileResponse:
                profile = await self.profile_repo.get_profile()
                return GetProfileResponse.from_entity(profile)
                
    Notes:
        - Use cases are async to support async repositories
        - Use cases should not contain UI logic or HTTP details
        - Use cases orchestrate entities and repositories
        - Validation can happen at DTO level or within use case
    """

    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        """
        Execute the use case with the given request.
        
        Args:
            request: The input data/command
            
        Returns:
            The result of the operation
            
        Raises:
            DomainError: For business rule violations
            ValidationError: For invalid input (if not caught at DTO level)
            
        Notes:
            - Should be idempotent when possible
            - Should handle errors gracefully
            - Should log important operations
            - Should use transactions when needed (future)
        """
        pass


class IQueryUseCase(ABC, Generic[TRequest, TResponse]):
    """
    Query Use Case Interface.
    
    Specialized interface for read-only operations (queries).
    Follows CQRS (Command Query Responsibility Segregation) pattern.
    
    Type Parameters:
        TRequest: The query parameters
        TResponse: The query result
        
    Usage:
        class GetAllSkillsQuery(IQueryUseCase[GetAllSkillsRequest, GetAllSkillsResponse]):
            async def execute(self, request: GetAllSkillsRequest) -> GetAllSkillsResponse:
                # Read-only operation
                ...
                
    Notes:
        - Queries should never modify state
        - Can be cached more aggressively
        - Can be optimized differently than commands
    """

    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        """
        Execute the query with the given parameters.
        
        Args:
            request: The query parameters
            
        Returns:
            The query result
            
        Notes:
            - Should not modify any state
            - Should be fast and cacheable
            - Should handle pagination when needed
        """
        pass


class ICommandUseCase(ABC, Generic[TRequest, TResponse]):
    """
    Command Use Case Interface.
    
    Specialized interface for write operations (commands).
    Follows CQRS (Command Query Responsibility Segregation) pattern.
    
    Type Parameters:
        TRequest: The command data
        TResponse: The command result (may be void/success status)
        
    Usage:
        class CreateProfileCommand(ICommandUseCase[CreateProfileRequest, CreateProfileResponse]):
            async def execute(self, request: CreateProfileRequest) -> CreateProfileResponse:
                # Write operation
                ...
                
    Notes:
        - Commands modify state
        - Should validate business rules
        - Should use transactions when needed
        - May trigger events/notifications
    """

    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        """
        Execute the command with the given data.
        
        Args:
            request: The command data
            
        Returns:
            The command result
            
        Raises:
            DomainError: For business rule violations
            
        Notes:
            - Should validate all business rules
            - Should be transactional when needed
            - Should update all affected aggregates
        """
        pass


class IValidator(ABC, Generic[TRequest]):
    """
    Validator Interface.
    
    Defines the contract for request validation.
    Can be used by use cases to validate input before processing.
    
    Type Parameters:
        TRequest: The request type to validate
        
    Usage:
        class CreateProfileValidator(IValidator[CreateProfileRequest]):
            def validate(self, request: CreateProfileRequest) -> List[str]:
                errors = []
                if not request.name:
                    errors.append("Name is required")
                return errors
    """

    @abstractmethod
    def validate(self, request: TRequest) -> list[str]:
        """
        Validate the request.
        
        Args:
            request: The request to validate
            
        Returns:
            List of error messages (empty if valid)
            
        Notes:
            - Should check all validation rules
            - Should return clear error messages
            - Should not throw exceptions (return errors instead)
        """
        pass
"""
Script to validate that all interfaces can be imported correctly.
This ensures there are no circular import issues.
"""

import os 
import sys 

# Add project root to PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

# Test 1: Import interfaces module
print("Testing interfaces imports...")
from app.shared.interfaces import (
    ICommandUseCase,
    IContactMessageRepository,
    IDTOMapper,
    IMapper,
    IOrderedRepository,
    IProfileRepository,
    IQueryUseCase,
    IRepository,
    ISocialNetworkRepository,
    IUniqueNameRepository,
    IUseCase,
    IValidator,
    IValueObjectMapper,
)

print("✓ All interface imports successful")

# Test 2: Import type aliases
print("\nTesting type alias imports...")
from app.shared.interfaces import (
    AdditionalTrainingRepository,
    CertificationRepository,
    ContactInformationRepository,
    ContactMessageRepository,
    EducationRepository,
    ProfileRepository,
    ProjectRepository,
    SkillRepository,
    SocialNetworkRepository,
    ToolRepository,
    WorkExperienceRepository,
)

print("✓ All type alias imports successful")

# Test 3: Import shared module
print("\nTesting shared module imports...")
from app.shared import (
    IMapper as Map,
)
from app.shared import (
    IRepository as Repo,
)
from app.shared import (
    IUseCase as UC,
)

print("✓ Shared module imports successful")

# Test 4: Import exceptions
print("\nTesting exception imports...")
from app.shared.exceptions import (
    ApplicationException,
    DuplicateException,
    NotFoundException,
    ValidationException,
)

print("✓ Exception imports successful")

# Test 5: Import types
print("\nTesting type imports...")
from app.shared.types import ID, Document, Timestamp

print("✓ Type imports successful")

print("\n" + "=" * 50)
print("✅ ALL IMPORTS VALIDATED SUCCESSFULLY")
print("=" * 50)

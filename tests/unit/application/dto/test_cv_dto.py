"""Tests for CV DTOs."""

from app.application.dto.cv_dto import CompleteCVResponse, GenerateCVPDFRequest

from .conftest import DT_END, DT_START, make_entity


def _make_profile():
    return make_entity(
        id="p-1",
        name="John",
        headline="Dev",
        bio=None,
        location=None,
        avatar_url=None,
    )


def _make_experience(**overrides):
    defaults = {
        "id": "w-1",
        "profile_id": "p-1",
        "role": "Dev",
        "company": "Acme",
        "start_date": DT_START,
        "end_date": DT_END,
        "description": None,
        "responsibilities": [],
        "order_index": 0,
    }
    defaults.update(overrides)
    entity = make_entity(**defaults)
    entity.is_current_position.return_value = False
    return entity


def _make_skill(**overrides):
    defaults = {
        "id": "s-1",
        "profile_id": "p-1",
        "name": "Python",
        "category": "backend",
        "order_index": 0,
        "level": None,
    }
    defaults.update(overrides)
    return make_entity(**defaults)


def _make_education(**overrides):
    defaults = {
        "id": "e-1",
        "profile_id": "p-1",
        "institution": "MIT",
        "degree": "BSc",
        "field": "CS",
        "start_date": DT_START,
        "end_date": DT_END,
        "description": None,
        "order_index": 0,
    }
    defaults.update(overrides)
    entity = make_entity(**defaults)
    entity.is_ongoing.return_value = False
    return entity


class TestCompleteCVResponseCreate:
    def test_composes_all_sections(self):
        profile = _make_profile()
        experiences = [_make_experience()]
        skills = [_make_skill(), _make_skill(id="s-2", name="FastAPI")]
        education = [_make_education()]

        resp = CompleteCVResponse.create(
            profile=profile,
            work_experiences=experiences,
            skills=skills,
            education=education,
        )

        assert resp.profile.id == "p-1"
        assert resp.profile.name == "John"
        assert len(resp.work_experiences) == 1
        assert resp.work_experiences[0].role == "Dev"
        assert len(resp.skills) == 2
        assert resp.skills[1].name == "FastAPI"
        assert len(resp.education) == 1
        assert resp.education[0].institution == "MIT"
        assert resp.contact_info is None
        assert resp.social_networks == []
        assert resp.projects == []
        assert resp.tools == []
        assert resp.additional_training == []
        assert resp.certifications == []

    def test_empty_sections(self):
        profile = _make_profile()
        resp = CompleteCVResponse.create(
            profile=profile,
            work_experiences=[],
            skills=[],
            education=[],
        )

        assert resp.profile.id == "p-1"
        assert resp.work_experiences == []
        assert resp.skills == []
        assert resp.education == []
        assert resp.contact_info is None
        assert resp.social_networks == []


class TestGenerateCVPDFRequest:
    def test_defaults(self):
        req = GenerateCVPDFRequest()
        assert req.format == "standard"
        assert req.include_photo is True

    def test_custom_values(self):
        req = GenerateCVPDFRequest(format="compact", include_photo=False)
        assert req.format == "compact"
        assert req.include_photo is False

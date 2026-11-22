import pytest

from api.incident import create_incident_from_transcript, redact_pii
from api.scoring import classify_severity


def test_unconfigured_provider_fails_closed():
    with pytest.raises(RuntimeError, match="not configured"):
        create_incident_from_transcript("API down")


def test_utc_timestamp_and_requested_timezone():
    incident = create_incident_from_transcript("Something is wrong", timezone="Asia/Tokyo", allow_fallback=True)
    assert incident["timezone"] == "Asia/Tokyo"
    assert incident["reported_at"].endswith("+00:00")


@pytest.mark.parametrize("text,expected", [
    ("minor issue, not urgent", "sev4"),
    ("non-critical cosmetic issue", "sev4"),
    ("download button looks odd", "sev3"),
    ("not urgent, but production API is down", "sev1"),
])
def test_severity_boundaries(text, expected):
    assert classify_severity({"category": "other"}, text) == expected


def test_supported_pii_patterns_removed_before_provider(monkeypatch):
    import api.incident as module
    captured = []

    def unavailable(text, call_id):
        captured.append(text)
        raise NotImplementedError

    monkeypatch.setattr(module, "call_llm_for_incident", unavailable)
    incident = create_incident_from_transcript(
        "Patient John Doe, phone 555-1234, email john@example.com reported an issue.", allow_fallback=True
    )
    for value in [captured[0], incident["title"], incident["summary"]]:
        assert "John Doe" not in value
        assert "555-1234" not in value
        assert "john@example.com" not in value
    assert incident["pii"] == {"contains_pii": True, "redaction_applied": True}


def test_clean_text_unchanged():
    assert redact_pii("API is down") == ("API is down", False)

"""Regression tests for the offline keyword router in backend/main.py.

The router's own comments document repeated past misroutes; these tests
pin the fixed behaviour so a future edit cannot silently reintroduce
them. The router is pure (no API key needed), and the history validator
is exercised through the ChatRequest model.
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent))

import main as backend_main
from main import ChatRequest, app, get_local_response


def test_health_endpoint_reports_status_and_llm_flag():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    # Only a boolean is exposed, never the key itself.
    assert isinstance(data["llm_configured"], bool)


def _intent(query: str) -> str:
    return get_local_response(query).intent


def test_machine_learning_routes_to_skills_not_education():
    # "machine learning" contains "learn", so a substring match used to
    # hit the education branch instead of skills.
    assert _intent("Tell me about machine learning") == "skills"


def test_bottom_does_not_route_to_projects():
    # "bottom" contains "bot", so a substring match used to hit the
    # projects branch.
    assert _intent("scroll to the bottom") == "general"


def test_how_does_it_work_routes_to_general_not_resume():
    # Bare "work" used to sit in the resume keyword list, so "How does
    # it work?" (work as a verb) routed to the resume timeline.
    assert _intent("How does it work?") == "general"


def test_github_projects_routes_to_projects_not_contact():
    # Project queries contain contact keywords ("show my GitHub
    # projects" contains "github"), so projects are checked first.
    assert _intent("show my GitHub projects") == "projects"


def test_email_agent_project_routes_to_projects_not_contact():
    # "AI Email Auto-Responder Agent" contains "email", which used to
    # misroute to the contact card instead of projects.
    assert _intent("Tell me about the AI Email Auto-Responder Agent") == "projects"


def test_plain_email_routes_to_contact():
    assert _intent("What is your email?") == "contact"


def test_bare_greeting_gets_a_greeting_reply():
    assert _intent("Hello!") == "general"
    assert get_local_response("Hello!").ai_text.startswith("Hello!")
    assert get_local_response("Hi").ai_text.startswith("Hello!")


def test_hi_does_not_match_his():
    # The greeting matcher must not steal "his": "what is his work
    # experience" still routes to the resume timeline.
    assert _intent("What is his work experience?") == "resume"


def test_greeting_with_intent_still_routes_to_the_intent():
    assert _intent("Hi, show me your projects") == "projects"


def test_education_and_experience_phrases_still_route():
    assert _intent("Where did you study?") == "general"
    assert _intent("Tell me about your work experience") == "resume"
    assert _intent("What are your skills in Python?") == "skills"


def test_history_validator_keeps_only_recent_messages():
    # 40 short messages: only the most recent 30 survive.
    history = [
        {"role": "user", "content": f"message {i}"} for i in range(40)
    ]
    request = ChatRequest(query="hello", history=history)

    assert len(request.history) == 30
    assert request.history[0].content == "message 10"
    assert request.history[-1].content == "message 39"


def test_history_validator_respects_character_budget():
    # 30 messages of 1000 chars each far exceed the 12000-char budget:
    # only the newest messages within budget are kept.
    history = [
        {"role": "user", "content": "x" * 1000} for _ in range(30)
    ]
    request = ChatRequest(query="hello", history=history)

    total = sum(len(msg.content) for msg in request.history)
    assert total <= ChatRequest.MAX_HISTORY_CHARS
    assert len(request.history) == 12


def test_history_validator_always_keeps_the_newest_message():
    # Even a single message over the budget must survive, so a long
    # question is never dropped. (A >12000-char message cannot arrive
    # through the public model — content caps at 4000 — so call the
    # validator directly with an unvalidated message.)
    from main import ChatMessageModel

    long_msg = ChatMessageModel.model_construct(role="user", content="y" * 20000)
    kept = ChatRequest.keep_recent_history([long_msg])

    assert kept == [long_msg]


def test_blank_query_and_blank_message_are_rejected():
    with pytest.raises(Exception):
        ChatRequest(query="   ", history=[])
    with pytest.raises(Exception):
        ChatRequest(query="hello", history=[{"role": "user", "content": "  "}])


def _reset_rate_limit():
    # The limiter is per-IP in memory and TestClient always connects
    # from the same address, so a test that exhausts the budget would
    # 429 every later chat test in this process. Reset between tests
    # (slowapi keeps the store on the private _storage attribute).
    backend_main.limiter._storage.reset()


def test_chat_endpoint_answers_offline_without_a_key(monkeypatch):
    # No GROQ_API_KEY in the test environment, but force the offline
    # path explicitly so this test never calls the LLM even if a key
    # is ever set where tests run.
    monkeypatch.setattr(backend_main, "client", None)
    _reset_rate_limit()
    with TestClient(app) as client:
        response = client.post("/api/chat", json={"query": "hello"})

    assert response.status_code == 200
    assert response.json()["intent"] == "general"


def test_chat_endpoint_rate_limits_after_30_requests_per_minute(monkeypatch):
    # The endpoint costs Groq quota, so an open URL must not be
    # hammerable: 30 requests in a minute pass, the 31st is rejected.
    monkeypatch.setattr(backend_main, "client", None)
    _reset_rate_limit()
    with TestClient(app) as client:
        statuses = [
            client.post("/api/chat", json={"query": "hello"}).status_code
            for _ in range(31)
        ]

    assert statuses[:30] == [200] * 30
    assert statuses[30] == 429

    # A 429 must say when to retry (RFC 7231 §7.1.3); the window is one
    # minute, so the header says 60 seconds.
    with TestClient(app) as client:
        response = client.post("/api/chat", json={"query": "hello"})
    assert response.status_code == 429
    assert response.headers["retry-after"] == "60"

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


def test_pytorch_django_and_yolo_questions_route_to_skills():
    # PyTorch, Django and YOLO are on his LinkedIn headline but were
    # missing from the knowledge base and both routers, so "Do you know
    # PyTorch?" fell through to the generic reply that omits them.
    assert _intent("Do you know PyTorch?") == "skills"
    assert _intent("Have you used Django?") == "skills"
    assert _intent("What about YOLO object detection?") == "skills"
    reply = get_local_response("Do you know PyTorch?")
    assert "PyTorch" in reply.ai_text
    assert "Django" in reply.ai_text
    assert "YOLO" in reply.ai_text


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


def test_ark_ai_routes_to_general_not_me():
    # "tell me about ARK AI" contains "about", so it used to hit the
    # "me" branch instead of answering about the company.
    assert _intent("Tell me about ARK AI") == "general"
    assert "February 2023" in get_local_response("Tell me about ARK AI").ai_text


def test_what_is_your_name_routes_to_me_not_generic():
    # "What is your name?" is an about-me question, but it used to fall
    # through to the generic reply. "your name" as a phrase must not
    # steal project or company questions, which are caught earlier.
    assert _intent("What is your name?") == "me"
    assert _intent("What is the name of the Facial Emotion Recognition System?") == "projects"
    assert _intent("What is the name of your company?") == "general"


def test_traffic_sign_question_routes_to_projects_not_me():
    # "Tell me about the traffic sign classifier" contains "about",
    # so it used to hit the "me" branch instead of projects.
    assert _intent("Tell me about the traffic sign classifier") == "projects"
    assert _intent("What is the traffic sign demo?") == "projects"
    assert _intent("Tell me about the traffic sign classification model") == "projects"


def test_founder_question_answers_about_ark_ai():
    assert _intent("Who founded ARK AI?") == "general"
    assert "ARK AI" in get_local_response("Who founded ARK AI?").ai_text
    assert _intent("What is your startup?") == "general"


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


def test_history_over_50_messages_validates_and_trims():
    # A long session sends more than 50 messages; the old max_length=50
    # rejected those with 422, so every question past 25 exchanges lost
    # its LLM answer and silently fell back to the local router.
    history = [
        {"role": "user", "content": f"message {i}"} for i in range(60)
    ]
    request = ChatRequest(query="hello", history=history)

    assert len(request.history) == 30
    assert request.history[0].content == "message 30"
    assert request.history[-1].content == "message 59"


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


def test_chat_endpoint_accepts_long_history(monkeypatch):
    # 26 exchanges = 52 history messages: the old max_length=50 answered
    # this with 422, and the frontend silently fell back to local replies
    # for the rest of the session.
    monkeypatch.setattr(backend_main, "client", None)
    _reset_rate_limit()
    history = [{"role": "user", "content": f"message {i}"} for i in range(52)]
    with TestClient(app) as client:
        response = client.post("/api/chat", json={"query": "hello", "history": history})

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


def test_configured_groq_model_is_not_the_retired_llama_id():
    # Groq shut llama-3.3-70b-versatile down for free/developer-tier use
    # on 16 Aug 2026; calling it returns model_not_found and every chat
    # silently falls back to the local router. Pin the configured model
    # to Groq's named replacement so a future edit cannot reintroduce it.
    assert backend_main.GROQ_MODEL == "openai/gpt-oss-120b"


def test_chat_endpoint_calls_the_configured_groq_model(monkeypatch):
    # The LLM call must use the configured model id, not a stale literal
    # buried in the call site.
    captured = {}

    class FakeMessage:
        content = '{"intent": "general", "ai_text": "hi there"}'

    class FakeChoice:
        message = FakeMessage()

    class FakeCompletion:
        choices = [FakeChoice()]

    class FakeCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)
            return FakeCompletion()

    class FakeChat:
        completions = FakeCompletions()

    class FakeClient:
        chat = FakeChat()

    monkeypatch.setattr(backend_main, "client", FakeClient())
    _reset_rate_limit()
    with TestClient(app) as client:
        response = client.post("/api/chat", json={"query": "hello"})

    assert response.status_code == 200
    assert captured.get("model") == backend_main.GROQ_MODEL == "openai/gpt-oss-120b"
    assert captured.get("response_format") == {"type": "json_object"}


def _client_with_llm_content(monkeypatch, content, choices=None):
    """Install a fake Groq client returning *content* as the LLM reply.

    choices defaults to a single choice carrying the content; pass []
    to simulate an empty choices list.
    """

    class FakeMessage:
        pass

    class FakeChoice:
        message = FakeMessage()

    FakeChoice.message.content = content

    class FakeCompletion:
        pass

    FakeCompletion.choices = [FakeChoice()] if choices is None else choices

    class FakeCompletions:
        def create(self, **kwargs):
            return FakeCompletion()

    class FakeChat:
        completions = FakeCompletions()

    class FakeClient:
        chat = FakeChat()

    monkeypatch.setattr(backend_main, "client", FakeClient())


def _post_chat(query):
    _reset_rate_limit()
    with TestClient(app) as client:
        return client.post("/api/chat", json={"query": query})


def test_malformed_llm_json_falls_back_to_local_router(monkeypatch):
    # A model reply that is not JSON used to be handled by the generic
    # fallback, but nothing pinned that: the endpoint must still answer
    # 200 with the local router's reply, not a 500.
    _client_with_llm_content(monkeypatch, '{"not json')

    response = _post_chat("hello")

    assert response.status_code == 200
    assert response.json()["intent"] == "general"


def test_empty_llm_choices_fall_back_to_local_router(monkeypatch):
    # choices[0] on an empty list raises IndexError inside the LLM
    # branch; the endpoint must recover with the local router.
    _client_with_llm_content(monkeypatch, "unused", choices=[])

    response = _post_chat("hello")

    assert response.status_code == 200
    assert response.json()["intent"] == "general"


def test_llm_intent_is_normalised_and_unknown_intents_fall_back(monkeypatch):
    # "Projects" (capitalised) must reach the projects intent, while an
    # unknown intent and an empty ai_text fall back to the general
    # intent with the default "not quite sure" text.
    _client_with_llm_content(
        monkeypatch, '{"intent": "Projects", "ai_text": "hi"}'
    )

    response = _post_chat("show me your projects")

    assert response.status_code == 200
    assert response.json()["intent"] == "projects"
    assert response.json()["ai_text"] == "hi"

    _client_with_llm_content(
        monkeypatch, '{"intent": "bogus", "ai_text": ""}'
    )

    response = _post_chat("hello")

    assert response.status_code == 200
    assert response.json()["intent"] == "general"
    assert response.json()["ai_text"] == "I'm not quite sure how to answer that."

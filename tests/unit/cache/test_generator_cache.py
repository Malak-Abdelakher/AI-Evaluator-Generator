import fakeredis

from cache.cache_service import CacheService
from cache.generator_cache import GeneratorCache


def create_generator_cache() -> GeneratorCache:
    fake_client = fakeredis.FakeRedis()

    cache_service = CacheService(
        client=fake_client,
        default_ttl=3600,
    )

    return GeneratorCache(
        cache=cache_service,
    )


def test_generator_cache_set_and_get():
    cache = create_generator_cache()

    cache.set(
        question="What is Redis used for?",
        context="Redis can be used as a caching layer.",
        history="",
        feedback="",
        model="llama3.1:latest",
        answer="Redis can be used as a caching layer.",
    )

    result = cache.get(
        question="What is Redis used for?",
        context="Redis can be used as a caching layer.",
        history="",
        feedback="",
        model="llama3.1:latest",
    )

    assert result == (
        "Redis can be used as a caching layer."
    )


def test_generator_cache_missing_entry_returns_none():
    cache = create_generator_cache()

    result = cache.get(
        question="Unknown question",
        context="",
        history="",
        feedback="",
        model="llama3.1:latest",
    )

    assert result is None


def test_generator_cache_feedback_changes_cache_key():
    cache = create_generator_cache()

    cache.set(
        question="Explain Redis.",
        context="Redis is used for caching.",
        history="",
        feedback="",
        model="llama3.1:latest",
        answer="First answer",
    )

    result = cache.get(
        question="Explain Redis.",
        context="Redis is used for caching.",
        history="",
        feedback="Make the answer clearer.",
        model="llama3.1:latest",
    )

    assert result is None


def test_generator_cache_history_changes_cache_key():
    cache = create_generator_cache()

    cache.set(
        question="Explain Redis.",
        context="Redis is used for caching.",
        history="",
        feedback="",
        model="llama3.1:latest",
        answer="First answer",
    )

    result = cache.get(
        question="Explain Redis.",
        context="Redis is used for caching.",
        history="Previous Generator attempt",
        feedback="",
        model="llama3.1:latest",
    )

    assert result is None


def test_generator_cache_context_changes_cache_key():
    cache = create_generator_cache()

    cache.set(
        question="What does Redis support?",
        context="Redis supports caching.",
        history="",
        feedback="",
        model="llama3.1:latest",
        answer="Redis supports caching.",
    )

    result = cache.get(
        question="What does Redis support?",
        context=(
            "Redis supports caching and "
            "session storage."
        ),
        history="",
        feedback="",
        model="llama3.1:latest",
    )

    assert result is None


def test_generator_cache_model_changes_cache_key():
    cache = create_generator_cache()

    cache.set(
        question="Explain caching.",
        context="Caching avoids repeated work.",
        history="",
        feedback="",
        model="llama3.1:latest",
        answer="Cached answer",
    )

    result = cache.get(
        question="Explain caching.",
        context="Caching avoids repeated work.",
        history="",
        feedback="",
        model="another-model",
    )

    assert result is None


def test_generator_cache_clear_removes_only_generator_entries():
    fake_client = fakeredis.FakeRedis()

    cache_service = CacheService(
        client=fake_client,
        default_ttl=3600,
    )

    generator_cache = GeneratorCache(
        cache=cache_service,
    )

    generator_cache.set(
        question="Question",
        context="Context",
        history="",
        feedback="",
        model="llama3.1:latest",
        answer="Answer",
    )

    cache_service.set(
        "retrieval:test-key",
        {"result": "keep me"},
    )

    deleted_count = generator_cache.clear()

    assert deleted_count == 1

    assert (
        generator_cache.get(
            question="Question",
            context="Context",
            history="",
            feedback="",
            model="llama3.1:latest",
        )
        is None
    )

    assert cache_service.get(
        "retrieval:test-key"
    ) == {
        "result": "keep me"
    }
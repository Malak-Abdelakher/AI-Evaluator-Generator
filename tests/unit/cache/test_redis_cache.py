import fakeredis

from cache.cache_service import CacheService


def create_cache(default_ttl: int = 3600) -> CacheService:
    fake_client = fakeredis.FakeRedis()
    return CacheService(
        client=fake_client,
        default_ttl=default_ttl,
    )


def test_cache_set_and_get():
    cache = create_cache()

    cache.set(
        "test:key",
        {"message": "hello", "count": 3},
    )

    result = cache.get("test:key")

    assert result == {
        "message": "hello",
        "count": 3,
    }


def test_cache_get_missing_key_returns_none():
    cache = create_cache()

    result = cache.get("missing:key")

    assert result is None


def test_cache_exists_and_delete():
    cache = create_cache()

    cache.set("test:key", "value")

    assert cache.exists("test:key") is True

    cache.delete("test:key")

    assert cache.exists("test:key") is False
    assert cache.get("test:key") is None


def test_cache_preserves_unicode_json():
    cache = create_cache()

    value = {
        "english": "Redis cache",
        "arabic": "ذاكرة التخزين المؤقت",
    }

    cache.set("unicode:key", value)

    assert cache.get("unicode:key") == value


def test_cache_delete_pattern():
    cache = create_cache()

    cache.set("retrieval:question-1", {"result": 1})
    cache.set("retrieval:question-2", {"result": 2})
    cache.set("generator:question-1", {"answer": "hello"})

    deleted_count = cache.delete_pattern("retrieval:*")

    assert deleted_count == 2

    assert cache.get("retrieval:question-1") is None
    assert cache.get("retrieval:question-2") is None

    # Other cache namespaces must remain untouched.
    assert cache.get("generator:question-1") == {
        "answer": "hello"
    }
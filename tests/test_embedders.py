"""The dummy embedder must be deterministic and shaped like the real one."""

from mailmind.embedders import DummyEmbedder


def test_dummy_embedder_returns_requested_dimension():
    emb = DummyEmbedder(dim=3072)
    vec = emb.embed("hello world")
    assert len(vec) == 3072


def test_dummy_embedder_is_deterministic():
    emb = DummyEmbedder(dim=64)
    assert emb.embed("same text") == emb.embed("same text")


def test_dummy_embedder_differs_by_text():
    emb = DummyEmbedder(dim=64)
    assert emb.embed("alpha") != emb.embed("beta")


def test_dummy_embedder_vectors_are_unit_normalized():
    emb = DummyEmbedder(dim=128)
    vec = emb.embed("normalize me")
    norm = sum(x * x for x in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-6


def test_similar_text_is_closer_than_unrelated_text():
    # word-overlap should make related texts more similar (cosine) than unrelated.
    emb = DummyEmbedder(dim=256)

    def cos(a, b):
        return sum(x * y for x, y in zip(a, b, strict=True))

    base = emb.embed("quarterly vendor contract payment terms")
    related = emb.embed("vendor contract payment review")
    unrelated = emb.embed("congratulations you won a free prize")

    assert cos(base, related) > cos(base, unrelated)

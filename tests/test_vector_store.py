import pytest
from database.vector_store import SyllabusVectorStore

def test_vector_store_initialization():
    store = SyllabusVectorStore(collection_name="test_syllabus")
    assert store.collection_name == "test_syllabus"

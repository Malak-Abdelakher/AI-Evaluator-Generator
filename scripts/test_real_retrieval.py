from knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)


knowledge = KnowledgePipeline.create_default()

result = knowledge.ingest_file(
    "tests/fixtures/sample.txt"
)

print("\nINGESTION RESULT")
print(result)

documents = knowledge.retrieve(
    "What can Redis be used for?",
    k=2,
)

print("\nRETRIEVED DOCUMENTS")

for document in documents:
    print("-" * 60)
    print(document.page_content)
    print(document.metadata)
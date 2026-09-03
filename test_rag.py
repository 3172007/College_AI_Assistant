import os

from services.vector_store import (
    create_vector_store,
    search_vector_store
)


# Find PDF
pdf_files = [
    file
    for file in os.listdir("documents")
    if file.lower().endswith(".pdf")
]


if not pdf_files:

    print("No PDF found.")

    exit()


pdf_path = os.path.join(
    "documents",
    pdf_files[0]
)


print("Creating vector store...")

index, chunks = create_vector_store(
    pdf_path
)


print("Vector store created successfully!")


question = input(
    "\nAsk a question: "
)


results = search_vector_store(
    index,
    chunks,
    question
)


print("\nRelevant Information:\n")


for result in results:

    print(result)

    print("\n--------------------\n")
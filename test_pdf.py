from services.search import search_pdf


pdf_path = "documents/geethu_resume.pdf"


question = input("Ask a question: ")


answer = search_pdf(
    pdf_path,
    question
)


print("\nAI Knowledge Result:")
print(answer)
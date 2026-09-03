from services.ai import generate_answer


question = "What are the technical skills?"


context = """
TECHNICAL SKILLS

Programming Languages:
Java, C, Python, SQL

Web Development:
HTML, CSS, JavaScript

Tools & Platforms:
Git & GitHub, VS Code, Kaggle

Core Concepts:
Data Structures, REST API basics,
Version Control
"""


answer = generate_answer(
    question,
    context
)


print("\nAI Answer:")
print(answer)
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

from models import db, Chat, Document

from services.vector_store import (
    create_vector_store,
    search_vector_store
)

from services.ai import generate_answer

from dotenv import load_dotenv

import os


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()


# =========================
# CREATE FLASK APP
# =========================

app = Flask(__name__)


# =========================
# SECRET KEY
# =========================

app.secret_key = os.getenv(
    "SECRET_KEY",
    "development-secret-key"
)


# =========================
# DATABASE CONFIGURATION
# =========================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///college_ai.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================
# CONNECT DATABASE
# =========================

db.init_app(app)


# =========================
# CREATE DATABASE TABLES
# =========================

with app.app_context():
    db.create_all()


# =========================
# CREATE RAG VECTOR STORE
# =========================

vector_index = None
vector_chunks = []


# Make sure documents folder exists
os.makedirs("documents", exist_ok=True)


# Find PDF files
pdf_files = [
    file
    for file in os.listdir("documents")
    if file.lower().endswith(".pdf")
]


# Create vector store from first PDF
if pdf_files:

    pdf_path = os.path.join(
        "documents",
        pdf_files[0]
    )

    print("Creating RAG vector store...")

    vector_index, vector_chunks = create_vector_store(
        pdf_path
    )

    print("RAG vector store ready!")


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================
# CHAT PAGE
# =========================

@app.route("/chat")
def chat():

    return render_template(
        "chat.html"
    )


# =========================
# CHAT API
# =========================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def api_chat():

    global vector_index
    global vector_chunks

    # Get JSON data
    data = request.get_json()

    # Get question
    question = data.get(
        "question",
        ""
    ).strip()


    # Check empty question
    if not question:

        return jsonify({
            "answer": "Please enter a question."
        })


    # =========================
    # CHECK RAG AVAILABILITY
    # =========================

    if vector_index is None:

        answer = (
            "No college document is available "
            "for answering this question."
        )


    else:

        # =========================
        # SEARCH RELEVANT DOCUMENT CHUNKS
        # =========================

        results = search_vector_store(
            vector_index,
            vector_chunks,
            question,
            top_k=3
        )


        # =========================
        # SEND CONTEXT TO OLLAMA AI
        # =========================

        if results:

            # Combine retrieved chunks
            context = "\n\n".join(
                results
            )

            try:

                answer = generate_answer(
                    question,
                    context
                )

            except Exception as e:

                print(
                    "AI Error:",
                    e
                )

                answer = (
                    "Sorry, I couldn't generate "
                    "an AI answer right now."
                )

        else:

            answer = (
                "I could not find relevant "
                "information in the documents."
            )


    # =========================
    # SAVE CHAT
    # =========================

    new_chat = Chat(
        question=question,
        answer=answer
    )

    db.session.add(
        new_chat
    )

    db.session.commit()


    # =========================
    # RETURN ANSWER
    # =========================

    return jsonify({
        "answer": answer
    })


# =========================
# ADMIN LOGIN
# =========================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )


        correct_username = os.getenv(
            "ADMIN_USERNAME"
        )

        correct_password = os.getenv(
            "ADMIN_PASSWORD"
        )


        # Check credentials
        if (
            username == correct_username
            and
            password == correct_password
        ):

            session[
                "admin_logged_in"
            ] = True

            return redirect(
                url_for(
                    "admin_dashboard"
                )
            )


        return render_template(
            "admin_login.html",
            error=(
                "Invalid username "
                "or password."
            )
        )


    return render_template(
        "admin_login.html"
    )


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin_dashboard():

    # Check login
    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for(
                "admin_login"
            )
        )


    # Get uploaded documents
    documents = Document.query.order_by(
        Document.uploaded_at.desc()
    ).all()


    return render_template(
        "admin.html",
        documents=documents
    )


# =========================
# PDF UPLOAD
# =========================

@app.route(
    "/admin/upload",
    methods=["POST"]
)
def admin_upload():

    # Check login
    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for(
                "admin_login"
            )
        )


    # Get uploaded file
    file = request.files.get(
        "document"
    )


    # Check file
    if not file:

        return redirect(
            url_for(
                "admin_dashboard"
            )
        )


    if file.filename == "":

        return redirect(
            url_for(
                "admin_dashboard"
            )
        )


    # =========================
    # ALLOW ONLY PDF
    # =========================

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        return (
            "Only PDF files are allowed.",
            400
        )


    # =========================
    # CREATE DOCUMENTS FOLDER
    # =========================

    os.makedirs(
        "documents",
        exist_ok=True
    )


    # File path
    filepath = os.path.join(
        "documents",
        file.filename
    )


    # Save file
    file.save(
        filepath
    )


    # =========================
    # SAVE DOCUMENT INFO
    # =========================

    document = Document(
        filename=file.filename
    )

    db.session.add(
        document
    )

    db.session.commit()


    return redirect(
        url_for(
            "admin_dashboard"
        )
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect(
        url_for(
            "home"
        )
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
import uuid
from typing import Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Quiz questions
questions = [
    {
        "id": 1,
        "text": "What is Azure primarily used for?",
        "options": ["Cloud Computing", "Web Development", "Database Management", "Mobile App Development"],
        "correct": "Cloud Computing"
    },
    {
        "id": 2,
        "text": "Which Azure service is used for serverless computing?",
        "options": ["Azure VM", "Azure Functions", "Azure SQL", "Azure Blob Storage"],
        "correct": "Azure Functions"
    },
    {
        "id": 3,
        "text": "What is the name of Azure's AI service?",
        "options": ["Azure Cognitive Services", "Azure Data Lake", "Azure DevOps", "Azure Kubernetes Service"],
        "correct": "Azure Cognitive Services"
    },
    {
        "id": 4,
        "text": "Which Azure service is used to store unstructured data?",
        "options": ["Azure SQL Database", "Azure Blob Storage", "Azure Virtual Machines", "Azure Functions"],
        "correct": "Azure Blob Storage"
    },
    {
        "id": 5,
        "text": "Which Azure service is used to implement Role-Based Access Control (RBAC) for managing access to Azure resources?",
        "options": ["Azure Active Directory", "Azure Key Vault", "Azure Policy", "Azure Monitor"],
        "correct": "Azure Active Directory"
}
    
]

# Server-side storage for user sessions and answers
sessions: Dict[str, Dict] = {}

def get_session(request: Request) -> str:
    """Get or create a session ID from a cookie."""
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        # Redirect to index if session is not found
        logger.warning("Session ID not found, redirecting to /")
        raise HTTPException(status_code=307, detail="Session not found, redirecting", headers={"Location": "/"})
    return session_id

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Create a new session when the quiz starts
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"current_question": 1, "answers": {}}
    logger.info(f"Quiz started, new session: {session_id}")

    # Set the session ID in a cookie
    response = templates.TemplateResponse("index.html", {"request": request})
    response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)  # Secure=True for HTTPS
    return response

@app.get("/question", response_class=HTMLResponse)
async def get_question(request: Request, session_id: str = Depends(get_session)):
    logger.info(f"GET question for session: {session_id}")
    
    # Get the current question ID from the session
    current_question_id = sessions[session_id]["current_question"]
    
    # Validate the current question ID
    if current_question_id < 1 or current_question_id > len(questions):
        logger.error(f"Invalid current question ID: {current_question_id}")
        raise HTTPException(status_code=404, detail="Invalid question")

    question = questions[current_question_id - 1]  # Convert to 0-based index
    return templates.TemplateResponse("question.html", {
        "request": request,
        "question": question,
        "qid": current_question_id,
        "total_questions": len(questions)
    })

@app.post("/question", response_class=HTMLResponse)
async def post_answer(request: Request, answer: str = Form(...), session_id: str = Depends(get_session)):
    logger.info(f"POST question for session: {session_id}, answer: {answer}")
    
    # Get the current question ID from the session
    current_question_id = sessions[session_id]["current_question"]
    
    # Validate the current question ID
    if current_question_id < 1 or current_question_id > len(questions):
        logger.error(f"Invalid current question ID: {current_question_id}")
        raise HTTPException(status_code=404, detail="Invalid question")
    
    # Store the answer
    sessions[session_id]["answers"][current_question_id] = answer
    logger.info(f"Stored answer for question {current_question_id}: {answer}")
    
    # Move to the next question
    if current_question_id < len(questions):
        sessions[session_id]["current_question"] += 1
        next_question_id = sessions[session_id]["current_question"]
        next_question = questions[next_question_id - 1]  # Convert to 0-based index
        logger.info(f"Rendering next question: {next_question_id}")
        return templates.TemplateResponse("question.html", {
            "request": request,
            "question": next_question,
            "qid": next_question_id,
            "total_questions": len(questions)
        })
    else:
        # Calculate score and show results
        user_answers = sessions[session_id]["answers"]
        score = sum(1 for i, q in enumerate(questions, 1) if user_answers.get(i) == q["correct"])
        logger.info(f"Quiz completed, score: {score}/{len(questions)}")
        return templates.TemplateResponse("results.html", {
            "request": request,
            "score": score,
            "total": len(questions),
            "questions": questions,
            "user_answers": user_answers
        })
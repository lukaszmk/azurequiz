from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging

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
    }
    {
    "id": 4,
    "text": "Which Azure service is used to manage virtual machines?",
    "options": ["Azure Virtual Network", "Azure Blob Storage", "Azure Virtual Machines", "Azure Functions"],
    "correct": "Azure Virtual Machines"
}
]

# Store user answers
user_answers = {}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    global user_answers
    user_answers = {}  # Reset answers on new quiz
    logger.info("Quiz started, user_answers reset")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/question/{qid}", response_class=HTMLResponse)
async def get_question(request: Request, qid: int):
    logger.info(f"GET question {qid}")
    if qid < 1 or qid > len(questions):
        logger.error(f"Invalid question ID: {qid}")
        return HTMLResponse("Invalid question", status_code=404)
    question = questions[qid-1]
    return templates.TemplateResponse("question.html", {
        "request": request,
        "question": question,
        "qid": qid,
        "total_questions": len(questions)
    })

@app.post("/question/{qid}", response_class=HTMLResponse)
async def post_answer(request: Request, qid: int, answer: str = Form(...)):
    logger.info(f"POST question {qid}, answer: {answer}")
    if qid < 1 or qid > len(questions):
        logger.error(f"Invalid question ID: {qid}")
        return HTMLResponse("Invalid question", status_code=404)
    
    # Store the answer
    user_answers[qid] = answer
    logger.info(f"Stored answer for question {qid}: {answer}")
    
    # Check if there are more questions
    if qid < len(questions):
        next_qid = qid + 1
        next_question = questions[next_qid - 1]  # Convert to 0-based index
        logger.info(f"Rendering next question: {next_qid}")
        return templates.TemplateResponse("question.html", {
            "request": request,
            "question": next_question,
            "qid": next_qid,
            "total_questions": len(questions)
        })
    else:
        # Calculate score and show results
        score = sum(1 for i, q in enumerate(questions, 1) if user_answers.get(i) == q["correct"])
        logger.info(f"Quiz completed, score: {score}/{len(questions)}")
        return templates.TemplateResponse("results.html", {
            "request": request,
            "score": score,
            "total": len(questions),
            "questions": questions,
            "user_answers": user_answers
        })
from fastapi import FastAPI, Form, Request, Response, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from requests import HTTPError
from starlette.responses import RedirectResponse



app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Timeout cookie duration in seconds
TIMEOUT_DURATION = 60

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
PATH_TO_CREDS = '/path/to/credentials/credentials/'
CLIENT_SECRET_FILE = PATH_TO_CREDS +'credentials.json'
 
def get_credentials():
    creds = None
    if os.path.exists(PATH_TO_CREDS +'token.json'):
        creds = Credentials.from_authorized_user_file(PATH_TO_CREDS +'token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request(scope=SCOPES))
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(PATH_TO_CREDS +'token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
 
 
def send_email(question1, question2, question3, email):
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(f"Survey Responses:\n1. {question1}\n2. {question2}\n3. {question3}\nEmail: {email}")
    message['to'] = 'abc123@gmail.com'
    message['from'] = 'abc123@gmail.com'
    message['subject'] = 'Survey Responses'

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message = {
            'raw': raw
            }

    try:
        message = (service.users().messages().send(userId="me", body=message).execute())
    except Exception as error:
        print(f'An error occurred: {error}')
            
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, timeout: int = Cookie(None)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit_survey(
    request: Request,
    response: Response,
    question1: str = Form(...),
    question2: str = Form(...),
    question3: str = Form(...),
    email: str = Form(None),
    ):
    
    timeout = request.cookies.get("timeout")
    if timeout and datetime.now() < datetime.fromtimestamp(int(timeout)):
        return {"message": "You are submitting too frequently. Please wait 60 seconds."}

    # Send email with survey responses
    send_email(question1, question2, question3, email)

    # Set timeout cookie
    response = RedirectResponse(url="/thank_you", status_code=303)
    response.set_cookie(key="timeout", value=str(int(datetime.now().timestamp() + TIMEOUT_DURATION)), httponly=True)
    return response

@app.get("/thank_you", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thank_you.html", {"request": request})

    
   

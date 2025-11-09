import os
import time
import datetime
import traceback
import base64
import requests
import webbrowser
import psutil
import google.generativeai as genai
import musiclibray
from dotenv import load_dotenv

load_dotenv()  # Load the .env  file
GENAI_KEY = os.getenv("GENAI_KEY")

genai.configure(api_key=GENAI_KEY)

model = genai.GenerativeModel("models/gemini-flash-latest")

try:
    from gtts import gTTS
    import pygame
except Exception:
    gTTS = None
    pygame = None

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from email.mime.text import MIMEText
except Exception:
    InstalledAppFlow = build = Credentials = Request = MIMEText = None


NEWSAPI_KEY = "3e24887dae7a43c68caadadd742b2c37"

if genai is not None:
    try:
        genai.configure = GENAI_KEY
    except Exception:
        pass


def aiprocess(command: str) -> str:
    """Call Gemini/GenAI to get a text response. Returns a fallback message on error."""
    try:
        if genai is None:
            return "AI backend not available (genai library not installed)."
        client = genai.GenerativeModel("models/gemini-flash-latest")
        response = client.generate_content(command)
        return getattr(response, "text", str(response))
    except Exception as e:
        return f"AI error: {str(e)}"


def get_battery_percentage() -> str:
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "Battery info not available on this system."
        percentage = int(battery.percent)
        plugged = battery.power_plugged
        status = "charging" if plugged else "not charging"
        return f"Battery: {percentage}% ({status})"
    except Exception as e:
        return f"Could not read battery: {e}"


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/calendar.readonly']

def gmail_login(credentials_path: str = "credentials.json", token_path: str = "token.json"):
    """Return a Gmail service object or an error string."""
    if build is None or InstalledAppFlow is None or Credentials is None:
        return "Google API libraries not installed."
    try:
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=8080)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        return f"Gmail login failed: {e}"

def generate_email_body(context: str) -> str:
    """Return AI-generated email body (best-effort)."""
    try:
        prompt = f"Write a professional email to a student informing them they are selected for {context}."
        if genai is None:
            return f"(AI not available) Professional email: Congratulations! You were selected for {context}."
        # If genai ChatCompletion available, adapt accordingly
        response = genai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message["content"]
    except Exception as e:
        return f"Failed to generate email: {e}"

def send_email(service_or_msg, to: str, subject: str, body: str):
    """Send email using Gmail service object (or return error text)."""
    try:
        if isinstance(service_or_msg, str):
            return f"Gmail error: {service_or_msg}"
        service = service_or_msg
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {"raw": raw}
        service.users().messages().send(userId="me", body=send_message).execute()
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {e}"


def open_website(url: str) -> str:
    try:
        webbrowser.open(url)
        return f"Opening {url}"
    except Exception as e:
        return f"Failed to open {url}: {e}"

def read_top_news(country: str = "us", max_articles: int = 5) -> str:
    try:
        if not NEWSAPI_KEY:
            return "News API key not configured."
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={NEWSAPI_KEY}")
        if r.status_code != 200:
            return f"News API error: {r.status_code}"
        data = r.json()
        articles = data.get("articles", [])[:max_articles]
        if not articles:
            return "No news found."
        headlines = [a.get("title", "No title") for a in articles]
        return " | ".join(headlines)
    except Exception as e:
        return f"Failed to fetch news: {e}"

def processCommand(command: str) -> dict:
    """Process a textual command and return a dict with 'message' and optional 'url'."""
    try:
        if not command or not isinstance(command, str):
            return {"message": "No command provided."}

        c = command.lower().strip()
        if "open google" in c:
            msg = open_website("https://google.com")
            return {"message": msg, "url": "https://google.com"}

        if "open youtube" in c:
            msg = open_website("https://youtube.com")
            return {"message": msg, "url": "https://youtube.com"}

        if "open instagram" in c:
            msg = open_website("https://instagram.com")
            return {"message": msg, "url": "https://instagram.com"}

        if "open amazon" in c:
            msg = open_website("https://amazon.com")
            return {"message": msg, "url": "https://amazon.com"}

        if "tell me the news" in c or "news" == c:
            return {"message": read_top_news()}
        # Battery
        if "battery" in c:
            return {"message": get_battery_percentage()}

        # Email
        if "send email" in c or "send an email" in c:
            return {"message": "To send email use /email endpoint."}

        if "check email" in c:
            svc = gmail_login()
            return {"message": svc if isinstance(svc, str) else "Gmail login successful."}
        
        if c.lower().startswith("play"):
           song = c.lower().split(" ")[1]
           link = musiclibray.music[song]
           webbrowser.open(link)

        if "ai" in c:
            reply = model.generate_content(command).text
            return {"message": reply}

        # Calendar
        if "calendar" in c or "events" in c:
            return {"message": "Calendar API not fully implemented in web mode."}

        if c in ("exit", "quit"):
            return {"message": "Goodbye."}

        # Default AI
        return {"message": aiprocess(command)}

    except Exception as e:
        tb = traceback.format_exc()
        return {"message": f"Error: {e}\n{tb}"}


if __name__ == "__main__":
    print("Main backend CLI tester. Type a command or 'quit'.")
    while True:
        cmd = input(">>> ").strip()
        if cmd in ("quit", "exit"):
            print("Bye.")
            break

        print(processCommand(cmd))  

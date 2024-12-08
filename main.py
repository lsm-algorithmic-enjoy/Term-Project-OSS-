from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found in environment variables")

client = OpenAI()

# GPT 모델에 전달할 시스템 프롬프트 정의
SYSTEM_PROMPT = """You are a professional music composer. 
Given a single keyword, create:
1. A short musical description (under 100 words)
2. A simple melody sequence using the notes: C4, D4, E4, F4, G4, A4, B4, C5
Format the response as JSON:
{
    "description": "musical description here",
    "notes": ["C4", "E4", "G4", ...],
    "durations": ["4n", "8n", "4n", ...],
    "tempo": 120
}
Keep the melody between 8-16 notes."""


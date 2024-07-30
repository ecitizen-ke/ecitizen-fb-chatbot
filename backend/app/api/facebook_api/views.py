from flask import Blueprint, request, jsonify, current_app
import requests
import json
from backend.extensions import db
from app.models import Message
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
import os
import fitz  # PyMuPDF

facebook_api_bp = Blueprint('facebook_api', __name__)

# Load the model and tokenizer globally
tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Load all FAQs from the local directory
faq_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'faqs')
faq_text = ""
for filename in os.listdir(faq_directory):
    if filename.endswith('.pdf'):
        faq_text += extract_text_from_pdf(os.path.join(faq_directory, filename))

@facebook_api_bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    elif request.method == 'POST':
        data = request.json
        process_incoming_message(data)
        return "ok", 200

def verify_fb_token(token_sent):
    if token_sent == current_app.config['VERIFY_TOKEN']:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

def process_incoming_message(data):
    for entry in data['entry']:
        for messaging_event in entry['messaging']:
            sender_id = messaging_event['sender']['id']
            if 'message' in messaging_event:
                message_text = messaging_event['message']['text']
                handle_message(sender_id, message_text)

def handle_message(sender_id, message_text):
    response_text = generate_response(message_text)
    send_message(sender_id, response_text)
    log_message(sender_id, message_text, response_text)

def generate_response(prompt):
    # Use the QA pipeline to generate a response with FAQ context
    result = qa_pipeline(question=prompt, context=faq_text)
    return result['answer']

def send_message(recipient_id, message_text):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text},
    }
    response = requests.post(f'https://graph.facebook.com/v11.0/me/messages?access_token={current_app.config["FB_PAGE_ACCESS_TOKEN"]}', headers=headers, data=json.dumps(data))
    return response.json()

def log_message(sender_id, message_text, response_text):
    message = Message(sender_id=sender_id, message_text=message_text, response_text=response_text)
    db.session.add(message)
    db.session.commit()
    
# from flask import Blueprint, request, jsonify, current_app
# import requests
# import json
# from backend.extensions import db
# from backend.app.models import Message
# from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
# import os
# import fitz  # PyMuPDF

# facebook_api_bp = Blueprint('facebook_api', __name__)

# # Load the model and tokenizer globally
# tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with fitz.open(pdf_path) as pdf:
#         for page in pdf:
#             text += page.get_text()
#     return text

# # Load all FAQs from the local directory
# faq_directory = os.path.join(os.path.dirname(__file__),'FAQs')
# faq_text = ""
# for filename in os.listdir(faq_directory):
#     if filename.endswith('.pdf'):
#         faq_text += extract_text_from_pdf(os.path.join(faq_directory, filename))

# @facebook_api_bp.route('/webhook', methods=['GET', 'POST'])
# def webhook():
#     if request.method == 'GET':
#         token_sent = request.args.get("hub.verify_token")
#         return verify_fb_token(token_sent)
#     elif request.method == 'POST':
#         data = request.json
#         process_incoming_message(data)
#         return "ok", 200

# def verify_fb_token(token_sent):
#     if token_sent == current_app.config['VERIFY_TOKEN']:
#         return request.args.get("hub.challenge")
#     return "Invalid verification token"

# def process_incoming_message(data):
#     for entry in data['entry']:
#         for messaging_event in entry['messaging']:
#             sender_id = messaging_event['sender']['id']
#             if 'message' in messaging_event:
#                 message_text = messaging_event['message']['text']
#                 handle_message(sender_id, message_text)

# def handle_message(sender_id, message_text):
#     response_text = generate_response(message_text)
#     send_message(sender_id, response_text)
#     log_message(sender_id, message_text, response_text)

# def generate_response(prompt):
#     # Use the QA pipeline to generate a response with FAQ context
#     result = qa_pipeline(question=prompt, context=faq_text)
#     return result['answer']

# def send_message(recipient_id, message_text):
#     headers = {
#         'Content-Type': 'application/json',
#     }
#     data = {
#         'recipient': {'id': recipient_id},
#         'message': {'text': message_text},
#     }
#     response = requests.post(f'https://graph.facebook.com/v11.0/me/messages?access_token={current_app.config["FB_PAGE_ACCESS_TOKEN"]}', headers=headers, data=json.dumps(data))
#     return response.json()

# def log_message(sender_id, message_text, response_text):
#     message = Message(sender_id=sender_id, message_text=message_text, response_text=response_text)
#     db.session.add(message)
#     db.session.commit()

import json
import requests
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

# Define the path to the saved model and tokenizer
model_path = '/home/mesfin/ecitizen-fb-chatbot/backend/fine_tuning/model_save'

# Load the model and tokenizer from the local path
# tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
# model = AutoModelForQuestionAnswering.from_pretrained('distilbert-base-uncased')
tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

# Comprehensive knowledge base
knowledge_base = {
    "Uwezo Fund Overview": (
        "Uwezo Fund is a government initiative established under The Public Finance Management Regulations in 2014. "
        "Its purpose is to empower women, youth, and persons with disabilities by expanding access to finance for starting and growing enterprises. "
        "The Fund aims to facilitate socio-economic transformation through financial support and capacity enhancement at the grassroots level."
    ),
    "Loan vs. Grant": (
        "Uwezo Fund provides loans, not grants. These loans are designed to empower women, youth, and persons with disabilities at the grassroots level."
    ),
    "Application Process": (
        "To apply for a Uwezo Fund Loan: "
        "1. Meet the eligibility criteria. "
        "2. Download and fill out the Loan Application Form from the Uwezo Fund website. "
        "3. Attach all required documents. "
        "4. Submit the completed form online through the Uwezo Fund website."
    ),
    "Constituency Management": (
        "At the constituency level, Uwezo Fund is managed by the Constituency Uwezo Fund Management Committee. "
        "This committee includes officers from the Uwezo Fund national office and representatives nominated by the local MP and County Women Representative."
    ),
    "Group Eligibility Criteria": (
        "To be eligible for Uwezo Fund Loans, a group must: "
        "1. Be registered with the Department of Social Services, Cooperatives, or the Registrar of Societies. "
        "2. Have members aged between 18 and 35 years for youth groups (for women and PWD groups, members must be above 18 years). "
        "3. Be based in the constituency where the application is made. "
        "4. Operate a table banking structure or similar group structure with evidence of monthly contributions. "
        "5. Have a registered bank account in the group's name."
    ),
    "Application Deadlines": (
        "There is no deadline for Uwezo Fund loan applications as it operates as a revolving fund."
    ),
    "Interest Rate and Repayment": (
        "Uwezo Fund Loans have an interest rate of 0% per annum. "
        "The repayment period is 24 months, with a 6-month grace period before the first repayment is due."
    ),
    "Institution Eligibility": (
        "Institutions applying for Uwezo Fund Loans must be registered entities with listed youth or women groups."
    ),
    "Group Existence Requirement": (
        "There is no minimum period required for a group's existence as long as it meets the Uwezo Fund eligibility criteria."
    ),
    "Funding Timeline": (
        "It takes approximately one month for a group to receive funding after submitting a loan application, following vetting and training."
    ),
    "Transparency Measures": (
        "To ensure transparency, Uwezo Fund displays beneficiary groups at NGCDF or Sub-County offices, and funds are disbursed in public forums."
    ),
    "Performance Improvement Focus": (
        "Key areas of focus for improving Uwezo Fund's performance include: "
        "1. Constituency-based loan recovery campaigns. "
        "2. Continuous awareness creation and public education. "
        "3. Ongoing training and follow-up of beneficiary groups. "
        "4. Strengthening the capacity of Constituency Uwezo Fund Management Committees. "
        "5. Enhancing partnership development."
    ),
    "Kenya Industrial Estates (KIE) Overview": (
        "Kenya Industrial Estates (KIE) is a parastatal and Development Finance Institution (DFI) under the Ministry of Co-operatives and MSME Development. "
        "KIE aims to support the development of Micro, Small, and Medium Enterprises (MSMEs) by promoting industrial clustering, entrepreneurship, and value addition."
    ),
    "KIE Mandate": (
        "KIE facilitates the industrial sector by: "
        "1. Promoting entrepreneurship through development finance. "
        "2. Incubating MSMEs to aid their growth. "
        "3. Supporting the graduation of micro and small enterprises to medium and large enterprises. "
        "4. Facilitating rural industrial development."
    ),
    "KIE Lending Programs": (
        "KIE offers the following lending programs: "
        "1. Small & Medium Scale Industry Loans: Ksh. 500,000 to Ksh. 20,000,000, repayable up to 8 years. "
        "2. Micro Loans: Ksh. 50,000 to Ksh. 500,000, repayable up to 4 years. "
        "3. Group Loans: For registered groups, between Ksh. 50,000 and Ksh. 500,000 on a graduation basis."
    ),
    "Interest Rate and Grace Period": (
        "KIE loans have an interest rate of 10% per annum on a reducing balance basis. "
        "A grace period of between three months and one year is available, especially for machinery purchases."
    ),
    "Requirements for Individual Loans": (
        "For individual loans from KIE, you need: "
        "1. Valid identification (ID, passport, driver's license). "
        "2. Proof of income (bank statements, payslips)."
    ),
    "Requirements for Business Loans": (
        "For business loans from KIE, you need: "
        "1. A business plan with objectives and financial projections. "
        "2. Collateral (property or equipment). "
        "3. Credit history. "
        "4. Legal documents (title deeds, business registration). "
        "5. Personal references."
    ),
    "Requirements for Limited Companies": (
        "For loans to limited companies from KIE, you need: "
        "1. Incorporation documents (certificate of incorporation, memorandum, articles of association). "
        "2. A detailed business plan with financial projections. "
        "3. Audited financial statements. "
        "4. Collateral. "
        "5. Credit history. "
        "6. Clear purpose for the loan. "
        "7. Legal compliance."
    ),
    "State Department for Performance and Delivery Management Overview": (
        "The State Department for Performance and Delivery Management is responsible for coordinating performance management in the Public Service, overseeing government ministries, departments, and agencies, and identifying innovative mechanisms for effective service delivery."
    ),
    "Technical Departments and Their Roles": (
        "1. Government Delivery Services Department: "
        "   - Tracks and reports on government priorities, projects, and programs. "
        "   - Solves challenges and provides interventions. "
        "   - Conducts independent verification of project status. "
        "   - Creates public awareness about progress and achievements through various media. "
        "2. Public Service Performance Management Department: "
        "   - Coordinates institutionalization of performance management. "
        "   - Monitors and evaluates performance. "
        "   - Ensures contracting parties meet agreed targets. "
        "3. Coordination & Supervision Services Department: "
        "   - Coordinates innovative mechanisms to address challenges. "
        "   - Maintains service delivery productivity. "
        "   - Designs measures to overcome service delivery challenges. "
        "   - Coordinates priority programs and projects. "
        "   - Conducts periodic assessments to enhance efficiency and effectiveness."
    ),
    "Performance Management": (
        "Performance management is a systematic process aimed at improving organizational results by managing achievement within a framework, guided by the Kenya Integrated Performance Management Policy."
    ),
    "Key Performance Management Tool": (
        "The key Performance Management tool adopted by the Government of Kenya is the Performance Contract. This is a negotiated agreement between a government agency and its owner, outlining mutual obligations, intentions, and responsibilities."
    ),
    "Why Performance Contracts?": (
        "Performance contracts are used to foster a culture of performance and accountability in public institutions. They commit officials to meet specified levels and effectively utilize resources to deliver goods and services."
    ),
    "Generally Accepted Performance Principles (GAPPs)": (
        "The 12 Generally Accepted Performance Principles (GAPPs) are: "
        "1. Appropriate Performance Measurement System. "
        "2. Appropriate Performance Measurement Methodology. "
        "3. Whole-of-Government Coverage. "
        "4. Accountability from Top-Down. "
        "5. Explicit and Unambiguous Assignment of Accountability. "
        "6. Appropriate Incentive System. "
        "7. Effective Integration with Human Resource Systems in Government. "
        "8. Integration with Budget System. "
        "9. Transparency. "
        "10. Appropriate Institutional Arrangements. "
        "11. Effective Communications Strategy. "
        "12. Strong and Unambiguous Legal Foundation."
    ),
    "Performance Contracting Guidelines": (
        "The Performance Contracting Guidelines assist public institutions in identifying performance indicators, negotiating, vetting, and implementing Performance Contracts, and evaluating their performance annually."
    ),
    "Cascading of Performance Contracts": (
        "Cascading of Performance Contracts extends Performance Contracting to all employees and downstream institutions, linking individual performance to strategic objectives and mandate achievement."
    ),
    "Performance Grade and Evaluation Report": (
        "Public institutions that achieve an 'Excellent' or 'Very Good' performance grade are eligible for rewards. Evaluation Reports, which detail these grades, can be accessed from the State Department's website."
    )
}

# Google Custom Search API credentials
API_KEY = 'AIzaSyDoDUITQKPsOC3w0QhYz9EIRZvC1f_dii0'
SEARCH_ENGINE_ID = 'e158394b07b3143d7'

def google_search(query):
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}'
    response = requests.get(url)
    search_results = response.json()
    return search_results.get('items', [])

def generate_response(prompt):
    # First, try to get the answer from the knowledge base
    response_text = get_answer_from_knowledge_base(prompt)
    
    # If no satisfactory answer is found, augment with web search results
    if not response_text:
        response_text = get_answer_from_web(prompt)
    
    return response_text

def get_answer_from_knowledge_base(prompt):
    # Search through the knowledge base for relevant information
    for title, context in knowledge_base.items():
        result = qa_pipeline(question=prompt, context=context)
        answer = result['answer']
        if answer:
            return f"Knowledge Base: {answer}"
    return None

def get_answer_from_web(prompt):
    # Perform a web search and return the first result
    search_results = google_search(prompt)
    if search_results:
        top_result = search_results[0]['snippet']
        return f"Web Search: {top_result}"
    return "I'm sorry, I couldn't find any relevant information on this subject."

def ask_question():
    while True:
        # Enter question
        question = input("Enter your question: ")
        if not question:
            print("Invalid input. Please enter a question.")
            continue
        
        # Get answer from the model
        response_text = generate_response(question)
        print(f"Question: {question}")
        print(f"Answer: {response_text}\n")

if __name__ == "__main__":
    ask_question()
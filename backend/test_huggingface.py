# import json
# from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

# # Define the path to the saved model and tokenizer
# model_path = '/home/mesfin/ecitizen-fb-chatbot/backend/fine_tuning/model_save'

# # Load the model and tokenizer from the local path
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForQuestionAnswering.from_pretrained(model_path)

# # Create a question-answering pipeline with the loaded model and tokenizer
# qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

# # Define the contexts based on your training data
# contexts = {
#     "eCitizen Overview": "eCitizen is the official digital payments platform that enables Kenyan citizens to access and pay for government services online. It offers services such as applying for passports, renewing driving licenses, business registration, and paying traffic fines.",
#     "Account Creation and Management": "To create an eCitizen account, visit the eCitizen portal and click on 'Create an Account'. Fill in the required details including your ID number, first name, and email address. Once your account is created, you can log in using your email and password. To reset your eCitizen password, go to the login page and click on 'Forgot Password'. Enter your registered email address and follow the instructions sent to your email to reset your password.",
#     "Passport Services": "To apply for a passport on eCitizen, log in to your account and select the 'Department of Immigration Services'. Choose 'Passport Application' and fill out the required details. Pay the application fee online and schedule an appointment for biometric capture. The passport application fee varies depending on the type of passport. A 32-page ordinary passport costs Ksh 4,550, while a 48-page ordinary passport costs Ksh 6,050. Diplomatic passports and other special types have different fees.",
#     "Driving License Renewal": "To renew your driving license on eCitizen, log in to your account and select the 'National Transport and Safety Authority'. Choose 'Driving License Renewal' and follow the instructions to complete the renewal process. You will need to pay the renewal fee online. The driving license renewal fee for a one-year license is Ksh 600, while a three-year license costs Ksh 1,400. These fees must be paid online through the eCitizen platform.",
#     "Business Registration": "To register a business on eCitizen, log in to your account and select the 'Business Registration Service'. Choose 'Business Name Registration' and fill out the required details. Pay the registration fee online and submit your application for processing. The registration fee for a business name on eCitizen is Ksh 950. This fee must be paid online through the eCitizen platform.",
#     "Traffic Fines Payment": "To pay a traffic fine on eCitizen, log in to your account and select the 'National Transport and Safety Authority'. Choose 'Traffic Fines Payment' and enter your ticket details. Follow the instructions to complete the payment online. The amount of a traffic fine varies depending on the violation. Traffic fines can be paid online through the eCitizen platform by entering the ticket details and following the payment instructions.",
#     "Huduma Namba": "Huduma Namba is a unique identification number issued to Kenyan citizens and foreign residents to facilitate the provision of government services. To register for Huduma Namba, visit the nearest Huduma Center with your identification documents."
# }

# def ask_question():
#     while True:
#         # Select context
#         print("\nSelect a context:")
#         for i, title in enumerate(contexts.keys(), 1):
#             print(f"{i}. {title}")
#         try:
#             context_index = int(input("Enter the number of the context (or 0 to exit): ")) - 1
#         except ValueError:
#             print("Invalid input. Please enter a number.")
#             continue
        
#         if context_index == -1:
#             break
        
#         if context_index < 0 or context_index >= len(contexts):
#             print("Invalid context number. Please try again.")
#             continue
        
#         context_title = list(contexts.keys())[context_index]
#         context = contexts[context_title]
        
#         # Enter question
#         question = input("Enter your question: ")
#         if not question:
#             print("Invalid input. Please enter a question.")
#             continue
        
#         # Get answer from the model
#         result = qa_pipeline(question=question, context=context)
#         print(f"Question: {question}")
#         print(f"Answer: {result['answer']}\n")

# if __name__ == "__main__":
#     ask_question()

import requests
from transformers import pipeline

# Google Custom Search API credentials
API_KEY = 'AIzaSyDoDUITQKPsOC3w0QhYz9EIRZvC1f_dii0'
SEARCH_ENGINE_ID = 'e158394b07b3143d7'

# Load summarization model
summarization_pipeline = pipeline('summarization')

def fetch_google_results(query):
    search_url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}'
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json()
        items = results.get('items', [])
        if items:
            return [item['snippet'] for item in items]
    return ['Unable to fetch data from Google.']

def summarize_text(text):
    # Summarize the combined results
    return summarization_pipeline(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']

def generate_coherent_answer(query):
    # Fetch search results
    search_results = fetch_google_results(query)
    
    if search_results:
        # Combine search results into a single text
        combined_results = ' '.join(search_results)
        
        # Summarize the combined results
        summary = summarize_text(combined_results)
        
        return summary
    else:
        return "Unable to retrieve information from the web."

def ask_question():
    while True:
        # Enter question
        question = input("Enter your question: ")
        if not question:
            print("Invalid input. Please enter a question.")
            continue
        
        # Generate a coherent answer
        answer = generate_coherent_answer(question)
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    ask_question()




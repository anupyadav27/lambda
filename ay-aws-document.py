import pytesseract
from PIL import Image
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from decouple import config
import os

# Step 1: Load your image
image_path = 'image.png'
img = Image.open(image_path)
openai_api_key = config('OPENAI_API_KEY')  # Ensure your OpenAI API key is set correctly

# Step 2: Extract text from the image using OCR (Tesseract)
extracted_text = pytesseract.image_to_string(img)
print("Extracted Text:", extracted_text)

# Step 3: Gather additional data from the user
questions = [
    "wWhat are the primary goals and expected benefits of this architecture?",
    "what we are proposing ? ",
    "High level of things to considered for Access & Security: What specific IAM roles and security measures are needed?",
    "Networking: what connectiivty needed ? Do we need F5 or ELB? Performance & DR: What is LVT requirment? specify in RPO terms",
    "Compliance & Licensing: What compliance standards must be met, and what licenses are required?",
    "Deployment Strategy: How will the deployment be automated, and what CI/CD practices will be used?",
    "High Availability: How is high availability ensured for each component, and why is it important for this solution?",
    "Scalability: How will the architecture handle scaling, and what mechanisms are in place to manage increased load?",
    "Any specific secuirty considertaion? ",
    "Does it need any migration of data or database or servers? what is approch ?",
    "DNS required?"
]

user_responses = {}
for question in questions:
    user_input = input(question + " ")
    user_responses[question] = user_input

# user_input = input("wWhat are the primary goals and expected benefits of this architecture?")
# insert multiple user input
# Step 4: Define the AWS Expert Agent's Task
# aws_instruction_template = """
# You are an AWS Cloud Expert. Analyze the following extracted text:
# '{text}'
# And consider the user's input:
# '{user_input}'
# # insert promt file
# Provide insights, best practices, and recommendations based on AWS cloud services. If any AWS-related code is present, explain its function and relevance.
# """
# prompt_file_path = 'prompt_file.txt'
# with open(prompt_file_path, "r") as file:
#     aws_instruction_template = file.read()
static_part = """
You are an AWS Cloud Expert. Analyze the following extracted text:
'{text}'
And consider the user's input:
'{user_input}'
"""

# Read the content from the prompt file
prompt_file_path = 'prompt_file.txt'
if os.path.exists(prompt_file_path):
    with open(prompt_file_path, 'r') as file:
        dynamic_part = file.read()  # Read content from prompt file
else:
    raise FileNotFoundError(f"{prompt_file_path} not found. Please check the file path.")

# Combine static and dynamic parts
aws_instruction_template = static_part + dynamic_part
aws_prompt_template = PromptTemplate(
    input_variables=["text", "user_input"],
    template=aws_instruction_template
)

aws_llmm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=openai_api_key)
aws_chain = LLMChain(llm=aws_llmm, prompt=aws_prompt_template)

# Step 5: Use AWS Expert Agent to Process the Extracted Text and User Input
aws_output = aws_chain.run(text=extracted_text, user_input=user_input)
print("AWS Expert Agent Processed Text:", aws_output)

# Step 6: Define the Technical Document Creator Agent's Task with Structured Document Sections
doc_instruction_template = """
You are a Technical Documentation Expert. Based on the following analysis from an AWS Cloud Expert:
'{aws_output}'
Create a structured technical document with the following sections:

## Summary
- Introduction
- Key Functionalities/Capabilities
- Assumptions/Constraints/Recommendations

## Solution Requirements
- User/Usage Requirements
- Interface Requirements
- Security Requirements
- Network Requirements
- Software Requirements
- Performance Requirements
- Supportability Requirements
- Storage Requirements
- Database Requirements
- Disaster Recovery Requirements
- Compliance Requirements
- Licensing Requirements
- Affinity/Anti-Affinity Requirements
- APM ID Tag
- Required Environments & LVT

## Proposed Solution
- Current Architecture - if any 
- Proposed New Architecture- describe the detailed new architecture design, components. Ask for more details from the user if needed.
- Pre-Production Architecture - specify whether it is the same as production or not. If different, ask for specifics.
- Production/DR Architecture - specify whether it is the same as production or not. If different, ask for specifics.
- EC2 Sizing/Specifications (Guidance on OS Volumes & MS Office Support)
- On-Prem Servers Sizing/Specifications (Constraints)
- Proposed Server Details
- WAS/Liberty/WebLogic JVM Requirements (Sample)
- F5 URLs
  - Current
  - New (Sample)
- Deployment Details - list high-level tasks and responsible teams.

## Miscellaneous Information - include any other relevant information.
"""

doc_prompt_template = PromptTemplate(
    input_variables=["aws_output"],
    template=doc_instruction_template
)

doc_llmm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=openai_api_key)
doc_chain = LLMChain(llm=doc_llmm, prompt=doc_prompt_template)

# Step 7: Use Technical Document Creator Agent to Generate the Work Document
final_document = doc_chain.run(aws_output=aws_output)
print("Generated Work Document:", final_document)

# Optionally, save the final document to a file
with open('work_document.txt', 'w', encoding='utf-8') as file:
    file.write(final_document)

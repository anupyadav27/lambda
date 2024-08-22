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
user_input = input("Please provide any specific details or requirements you'd like included in the document: ")

# Step 4: Define the AWS Expert Agent's Task
aws_instruction_template = """
You are an AWS Cloud Expert. Analyze the following extracted text:
'{text}'
And consider the user's input:
'{user_input}'
Provide insights, best practices, and recommendations based on AWS cloud services. If any AWS-related code is present, explain its function and relevance.
"""

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

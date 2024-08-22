import pytesseract
from PIL import Image
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from decouple import config
import openai
import os

# Step 1: Load your image
image_path = 'image.png'
img = Image.open(image_path)
openai_api_key = config('OPENAI_API_KEY')  # Ensure your OpenAI API key is set correctly

# Step 2: Extract text from the image using OCR (Tesseract)
extracted_text = pytesseract.image_to_string(img)
print("Extracted Text:", extracted_text)

# Step 3: Define the AWS Expert Agent's Task
aws_instruction_template = """
You are an AWS Cloud Expert. Analyze the following extracted text:
'{text}'
Provide insights, best practices, and recommendations based on AWS cloud services. If any AWS-related code is present, explain its function and relevance.
"""

aws_prompt_template = PromptTemplate(
    input_variables=["text"],
    template=aws_instruction_template
)

aws_llmm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=openai_api_key)
aws_chain = LLMChain(llm=aws_llmm, prompt=aws_prompt_template)

# Step 4: Use AWS Expert Agent to Process the Extracted Text
aws_output = aws_chain.run(text=extracted_text)
print("AWS Expert Agent Processed Text:", aws_output)

# Step 5: Define the Technical Document Creator Agent's Task
doc_instruction_template = """
You are a Technical Documentation Expert. Based on the following analysis from an AWS Cloud Expert:
'{aws_output}'
Create a structured technical document. Include sections such as Overview, Key Points, Technical Details, Recommendations, and any other relevant sections.
"""

doc_prompt_template = PromptTemplate(
    input_variables=["aws_output"],
    template=doc_instruction_template
)

doc_llmm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=openai_api_key)
doc_chain = LLMChain(llm=doc_llmm, prompt=doc_prompt_template)

# Step 6: Use Technical Document Creator Agent to Generate the Work Document
final_document = doc_chain.run(aws_output=aws_output)
print("Generated Work Document:", final_document)

# Optionally, save the final document to a file
with open('work_document.txt', 'w', encoding='utf-8') as file:
    file.write(final_document)

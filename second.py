# import pytesseract
# from PIL import Image
# from langchain_openai import OpenAI
# # from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# # Load your image
# image_path = 'image.png'
# img = Image.open(image_path)

# # Step 1: Extract text from the image using OCR (Tesseract)
# extracted_text = pytesseract.image_to_string(img)
# print("Extracted Text:", extracted_text)

# # Step 2: Use LangChain and GPT-4 to process the text
# # Define your OpenAI model (GPT-4 via OpenAI API)
# llm = OpenAI(temperature=0.7, model_name="gpt-4")

# # Create a prompt template for LangChain
# prompt_template = PromptTemplate(
#     input_variables=["text"],
#     template="You have extracted the following text from an image: '{text}'. Now, summarize it."
# )

# # Create the LangChain for processing
# chain = LLMChain(llm=llm, prompt=prompt_template)

# # Step 3: Feed the extracted text into the chain and get the output from GPT-4
# output = chain.run(text=extracted_text)
# print("Processed Text:", output)
import pytesseract
from PIL import Image
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config

# Step 1: Load your image
image_path = 'image.png'
img = Image.open(image_path)
openai_api_key = config('OPENAI_API_KEY')
# Step 2: Extract text from the image using OCR (Tesseract)
extracted_text = pytesseract.image_to_string(img)
print("Extracted Text:", extracted_text)

# Step 3: Use LangChain and GPT-4 to process the text
# Set your API key
# Define your OpenAI model (GPT-4 via OpenAI API)
llmm = OpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

# Create a prompt template for LangChain
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="You have extracted the following text from an image: '{text}'. Now, summarize it."
)

# Create the LangChain for processing
chain = LLMChain(llm=llmm, prompt=prompt_template)

# Step 4: Feed the extracted text into the chain and get the output from GPT-4
output = chain.run(text=extracted_text)
print("Processed Text:", output)


#     return final_document
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from decouple import config
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI API Key
openai_api_key = config('OPENAI_API_KEY')
# taking user response
def process_text_and_user_input(user_responses):
    static_part = """
    consider the user's input:
    '{user_input}'
    """
    # Convert user responses dictionary to a formatted string
    formatted_user_input = "\n".join([f"**{q}**\n{a}" for q, a in user_responses.items()])
    print(formatted_user_input)
    
    prompt_file_path = 'prompt_file.txt'
    
    if os.path.exists(prompt_file_path):
        try:
            with open(prompt_file_path, 'r') as file:
                dynamic_part = file.read()
        except Exception as e:
            logging.error(f"Error reading file {prompt_file_path}: {e}")
            raise
    else:
        raise FileNotFoundError(f"{prompt_file_path} not found. Please check the file path.")

    # aws_instruction_template = static_part + dynamic_part
    aws_prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template=dynamic_part
    )
# passing user input and prompt to call openai 
    
    try:
        aws_llmm = ChatOpenAI(temperature=0.5, model_name="gpt-4", openai_api_key=openai_api_key)
        aws_chain = LLMChain(llm=aws_llmm, prompt=aws_prompt_template)
        aws_output = aws_chain.run(user_input=formatted_user_input)
    except Exception as e:
        logging.error(f"Error generating output with OpenAI API: {e}")
        raise

    return aws_output

# def create_technical_document(aws_output):
#     doc_instruction_template = """
#     You are a Technical Documentation Expert. Based on :
#     '{aws_output}'
#     """
#     doc_prompt_template = PromptTemplate(
#         input_variables=["aws_output"],
#         template=doc_instruction_template
#     )

#     try:
#         doc_llmm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=openai_api_key)
#         doc_chain = LLMChain(llm=doc_llmm, prompt=doc_prompt_template)
#         final_document = doc_chain.run(aws_output=aws_output)
#     except Exception as e:
#         logging.error(f"Error generating technical document with OpenAI API: {e}")
#         raise

#     return final_document



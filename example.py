import json
import boto3
import requests
from PIL import Image
import io
import base64

# Initialize AWS clients
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')

# OpenAI API settings
openai_api_url = "https://api.openai.com/v1/chat/completions"
openai_api_key = "your-openai-api-key"

# S3 bucket names
source_bucket = 'your-source-bucket-name'
destination_bucket = 'your-destination-bucket-name'

def upload_image_to_s3(image_bytes, bucket_name, key):
    s3_client.put_object(Body=image_bytes, Bucket=bucket_name, Key=key)
    print(f"Image uploaded to {bucket_name}/{key}")

def process_image_with_rekognition(image_key):
    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': source_bucket,
                'Name': image_key,
            }
        },
        MaxLabels=10,
        MinConfidence=90
    )
    labels = response['Labels']
    return [label['Name'] for label in labels]

def get_gpt4_description(labels):
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {"role": "system", "content": "You are an expert image analyzer."},
        {"role": "user", "content": f"The following objects were detected in the image: {', '.join(labels)}. Can you generate a short description?"}
    ]
    
    payload = {
        "model": "gpt-4",
        "messages": messages,
        "max_tokens": 150
    }
    
    response = requests.post(openai_api_url, headers=headers, json=payload)
    response_data = response.json()
    return response_data['choices'][0]['message']['content'].strip()

def store_result_in_s3(image_key, labels, gpt4_summary):
    result = {
        "image": image_key,
        "labels": labels,
        "gpt4_summary": gpt4_summary
    }
    
    result_key = image_key.replace('.jpg', '_result.json')
    s3_client.put_object(
        Bucket=destination_bucket,
        Key=result_key,
        Body=json.dumps(result)
    )
    print(f"Processed result saved to {destination_bucket}/{result_key}")

def process_image(file_path):
    # Load image with Pillow
    with Image.open(file_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
    
    image_key = 'uploaded_image.jpg'
    
    # Upload image to S3
    upload_image_to_s3(img_bytes, source_bucket, image_key)
    
    # Process image with Rekognition
    labels = process_image_with_rekognition(image_key)
    
    # Generate description with GPT-4
    gpt4_summary = get_gpt4_description(labels)
    
    # Store the results in another S3 bucket
    store_result_in_s3(image_key, labels, gpt4_summary)

    return gpt4_summary

# Example usage
image_path = 'path_to_your_image.jpg'
description = process_image(image_path)
print(f"Image Description: {description}")

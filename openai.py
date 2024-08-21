import boto3
import base64
import json

# Initialize AWS clients
s3_client = boto3.client('s3')
bedrock_client = boto3.client('bedrock')

def lambda_handler(event, context):
    # Extract bucket name and object key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    print(bucket_name,object_key)
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()

    # Convert the image data to Base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    # Prepare the input payload for the Bedrock model
    input_payload = {
        "inputs": {
            "image": image_base64,
            "text": "What is in this image?"
        },
        "model": "gpt-4o",  # Ensure this is the correct model ID
        "output": {
            "type": "text"
        }
    }

    # Send the request to the Bedrock model
    bedrock_response = bedrock_client.invoke_model(
        modelId='gpt-4o',  # Replace with the correct model ID if different
        contentType='application/json',
        accept='application/json',
        body=json.dumps(input_payload)
    )

    # Parse the response from the model
    model_response = json.loads(bedrock_response['body'])
    return {
        'statusCode': 200,
        'body': json.dumps({'response': model_response['text']})
    }

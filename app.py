from flask import Flask, request, render_template, jsonify
import boto3
from botocore.exceptions import NoCredentialsError
import os
import base64

app = Flask(__name__)

# AWS region and bucket name
REGION = 'us-east-1'
BUCKET_NAME = 'bucketname1234'

# Initialize boto3 client for S3 and Rekognition
s3_client = boto3.client('s3', region_name=REGION)
rekognition_client = boto3.client('rekognition', region_name=REGION)

def list_images_in_s3(bucket_name):
    """List all images in the specified S3 bucket."""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            return []
    except NoCredentialsError:
        print("Credentials not available.")
        return []

def compare_faces(source_image, target_image):
    """Compare faces between the source and target images."""
    response = rekognition_client.compare_faces(
        SourceImage={'S3Object': {'Bucket': BUCKET_NAME, 'Name': source_image}},
        TargetImage={'S3Object': {'Bucket': BUCKET_NAME, 'Name': target_image}},
        SimilarityThreshold=90  # Adjust the similarity threshold as needed
    )
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json
    image_data = data['image']
    image_bytes = base64.b64decode(image_data.split(',')[1])
    
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, 'captured_image.png')
    
    with open(file_path, 'wb') as file:
        file.write(image_bytes)
    
    s3_client.upload_file(file_path, BUCKET_NAME, 'captured_image.png')
    os.remove(file_path)
    
    s3_images = list_images_in_s3(BUCKET_NAME)
    for s3_image in s3_images:
        if s3_image == 'captured_image.png':
            continue
        response = compare_faces('captured_image.png', s3_image)
        if response['FaceMatches']:
            return jsonify({"status": "Person authorized", "redirect": "/chat"})
    
    return jsonify({"status": "Person not authorized", "redirect": None})

data_array = [
    {'question': 'What is the capital of France?', 'answer': 'Paris'},
    {'question': 'What is the capital of Spain?', 'answer': 'Madrid'},
    {'question': 'What is the capital of Germany?', 'answer': 'Berlin'},
    {'question': 'CEO or founder of technical hub?', 'answer': 'Babji Neelam'},
    {'question': 'who is the trainer for aws devops who is the trainer of aws devops trainer', 'answer': 'Pavan Teja R,Aravind P'},
    {'question': 'where is aws devops class room of aws devops', 'answer': '2nd Floor Hall 2.2'},
    {'question': 'who is the trainer for servicenow who is the trainer of servicenow trainer', 'answer': 'Raja choudhary P D'},
    {'question': 'where is the servicenow class room of servicenow', 'answer': '2nd Floor 2.1'},
    {'question': 'where is the ceo cabin of ceo', 'answer': '3rd Floor'},
    {'question': 'where is the aws devolopment class room of aws development', 'answer': '4th Floor Hall 4.2'},
    {'question': 'where is the google flutter class room of google flutter', 'answer': '3rd Floor Bay 3.1'},
    {'question': 'where is the vlsi class room of vlsi', 'answer': '3rd Floor Bay 3.2'},
    {'question': 'where is the data analytics class room of data analytics', 'answer': '3rd Floor Bay 3.3'},
    {'question': 'where is the cloud3 class room of cloud3', 'answer': '3rd Floor Bay 3.4'},
    {'question': 'where is the salesforce class room of saleforce', 'answer': '3rd Floor Bay 3.5'},
    {'question': 'where is the fsd class room of fsd', 'answer': '4th Floor Hall 4.1'},
    {'question': 'where is the gen ai class room of gen ai', 'answer': '5th Floor ISLAND-1'},
    {'question': 'where is the cybersecurity class room of cybersecurity', 'answer': '5th Floor ISLAND-2'},
    {'question': 'where is the orecel apex class room of orecel apex', 'answer': '5th Floor ISLAND-3'},
    {'question': 'where is the uiux class room of uiux', 'answer': '5th Floor ISLAND-4'},
    {'question': 'where is the pega class room of pega', 'answer': '5th Floor ISLAND-5and Hall 5.2'},
    {'question': 'where is the owl coder class room of owl coder', 'answer': '5th Floor Hall 5.3'},
    {'question': 'who is the trainer for aws development who is the trainer of aws development aws development trainer', 'answer': 'shifu zama sir'},
    {'question': 'who is the trainer for google flutter who is the trainer for flutter google flutter trainer', 'answer': 'Kirshna and Vasanth sir'},
    {'question': 'who is the trainer for vlsi who is the trainer of vlsi trainer', 'answer': 'Ashok sir'},
    {'question': 'who is the trainer for data analytics who is the trainer of data analytics trainer', 'answer': 'Harsha Vardhini Madam'},
    {'question': 'who is the tariner for cloud3 who is the tariner of cloud3 trainer', 'answer': 'Arvind and Keshor sir'},
    {'question': 'who is the trainer for saleforce who is the trainer of saleforce trainer', 'answer': 'Marni Srinu Sir'},
    {'question': 'who is the tariner for fsd who is the tariner of fsd trainer', 'answer': 'Durga Sai Prasad and Hanuman Sir'},
    {'question': 'who is the trainer for gen ai who is the trainer of gen ai trainer', 'answer': 'Aravind Sir'},
    {'question': 'who is the trainer for cybersecurity who is the trainer of cybersecurity trainer', 'answer': 'Sai Kala Madam and J Peter Sir '},
    {'question': 'who is the trainer for pega who is the trainer of pega trainer', 'answer': 'Raja Choudhary and Muthyala Babu Sir'},
    {'question': 'bye thank you for information', 'answer': 'ok, Have a nice day. if you have any queries ask me about t hub'},
    {'question': 'hi hello hey oy Virtual Friend vfriend v friend maya', 'answer': 'Hi,welcome to Technical HUB ,How can i assist you?'},
    {'question': 'who is Pawan teja sir refer for', 'answer': 'aws cloud devops trainer'},
    {'question': 'who is Aravind sir refer for', 'answer': 'aws cloud devops trainer, cloud3 trainer,gen ai trainer'},
    {'question': 'who is babji neelam', 'answer': 'founder and CEO of TechnicalHub'},
    {'question': 'who is shifu zama sir refer for ', 'answer': 'aws development trainer,CCNA trainer'},
    {'question': 'who is Kirshna sir who is Vasanth sir', 'answer': 'google flutter trainer'},
    {'question': 'who is ashok sir refer for', 'answer': 'vlsi trainer'},
    {'question': 'who is Harsha Vardhini Madam refer for', 'answer': 'data analytics trainer'},
    {'question': 'who is Keshor sir', 'answer': 'cloud3 trainer'},
    {'question': ' who is Marni Srinu Sir', 'answer': 'saleforce trainer'},
    {'question': 'who is Durga Sai Prasad and Hanuman Sir', 'answer': 'fsd trainer'},
    {'question': 'who is Sai Kala Madam who is J Peter Sir', 'answer': 'cybersecurity trainer'},
    {'question': 'who is Raja Choudhary sir who is Muthyala Babu Sir', 'answer': 'pega trainer'},
    {'question': 'who are the interns for aws cloud devops who are the interns of aws cloud devops interns', 'answer': ' Anusha,aparna,gowtham'},
    
]

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    print('coming')
    print("hai")

    data = request.json
    user_message = data['message']

    # # Lex bot configuration
    # LEX_BOT_NAME = 'maya'
    # LEX_BOT_ALIAS = 'alliasama'
    # LEX_BOT_USER_ID = 'UBOXI0UKON'

    # lex_client = boto3.client('lex-runtime', region_name='us-east-1')
    # print(lex_client)



    for element in data_array:
        print(jsonify({"response": element['answer']}))
        if user_message.lower() in element['question'].lower():
            return jsonify({"response": element['answer']})


    
    return jsonify({"response": 'the data you provided is out of my knowledge, for more info cantact 8343818181 number or ping at6 support@technicalhub.io'})




if __name__ == "__main__":
    app.run(debug=True)

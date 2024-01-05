from chalice import Chalice, Response
import boto3
import json
from datetime import datetime

app = Chalice(app_name="feds_upload_api")

BUCKET = '**********'  # bucket name
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

@app.route("/healthcheck", api_key_required=True)
def index():
    return {"Status": "running"}

@app.route('/upload/{location}', methods=['POST'],
           content_types=['application/octet-stream'], api_key_required=True)
def upload_to_s3(location):

   #Set up filename and filepath
    time_stamp = datetime.now()
    time_stamp = time_stamp.strftime("%m_%d_%Y-%H_%M_%S")
    mdy, hms = time_stamp.split("-")
    id = "esp32"
    file_name =f"{hms}_{id}-{location}.jpg"

   #Update tmp file with image from Scout Drone
    body = app.current_request.raw_body
    tmp_file_name = '/tmp/' + file_name
    with open(tmp_file_name, 'wb') as tmp_file:
        tmp_file.write(body)

    #Upload tmp file to s3 bucket
    key = f"images/{mdy}/{file_name}"
    s3_client.upload_file(tmp_file_name, BUCKET, key)
    update_upload_file("True")
    return Response(body=id, status_code=200)

@app.route("/fetch", methods=['GET'], api_key_required=True)
def fetch_from_s3():

    #Fetches JSON file with fire detection inferences on uploaded image
    json_content = None
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix = "detection-json")
    files = response.get("Contents")
    key = None
    print(files)
    if len(files) > 1:
        key = files[1]['Key']
    if key:
        print("fetching json " + str(key))
        result = s3_client.get_object(Bucket = BUCKET, Key = key)
        text = result["Body"].read().decode("utf-8")
        print(text)
        json_content = json.loads(text)
        s3_client.delete_object(Bucket=BUCKET, Key=key)
    return json_content

@app.route("/check-ready", methods=["GET"], api_key_required=False)
def check_ready():
    ready = s3_client.get_object(Bucket=BUCKET, Key="ready/ready.txt")
    contents = ready['Body'].read().decode('utf-8')
    if contents == "True":
        update_ready_file("False")
    return contents

@app.route("/ready", methods=["GET"], api_key_required=False)
def ready():
    #Called by camera on ready
    update_ready_file("True")
    return "True"

@app.route("/check-upload", methods=["GET"], api_key_required = False)
def check_upload():
    upload = s3_client.get_object(Bucket=BUCKET, Key="picture_upload/picture_upload.txt")
    contents = upload["Body"].read().decode("utf-8")
    if contents == "True":
        update_upload_file("False")
    return contents

@app.route("/check-permit", methods=["GET"], api_key_required=False)
def check_permit():
    upload = s3_client.get_object(Bucket=BUCKET, Key="check_permit/check_permit.txt")
    contents = upload["Body"].read().decode("utf-8")
    return contents

def update_ready_file(content):
    tmp_file_name = '/tmp/ready.txt'
    with open(tmp_file_name, 'w') as tmp_file:
        tmp_file.write(content)
    s3_client.upload_file(tmp_file_name, Bucket=BUCKET, Key="ready/ready.txt")

def update_upload_file(content):
    tmp_file_name = '/tmp/picture_upload.txt'
    with open(tmp_file_name, 'w') as tmp_file:
        tmp_file.write(content)
    s3_client.upload_file(tmp_file_name, Bucket=BUCKET, Key="picture_upload/picture_upload.txt")

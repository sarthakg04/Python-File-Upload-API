#app.py
import os
#mport urllib.request

import boto3
from flask import Flask, json, jsonify, request

s3_client=boto3.client('s3',aws_access_key_id="#fill the bucket id",aws_secret_access_key="# fill the bucket access key")
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def main():
    return 'Homepage'
 
@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
    path = request.files.getlist('files[]') 
    errors = {}
    success = False
     
    for file in files:      
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response= s3_client.upload_file(os.path.join(app.config['UPLOAD_FOLDER'], filename),'sample-php-abhi','dummmysarthak.jpg')
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
 
if __name__ == '__main__':
    app.run(debug=True)

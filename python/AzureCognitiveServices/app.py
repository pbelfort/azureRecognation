import os
import time
import requests

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"

# Replace with a valid key
training_key = "REPLACE FOR A VALID TRAINING KEY (SAME AS app.py)"
prediction_key = "REPLACE FOR A VALID PREDICTION KEY"
prediction_resource_id = "REPLACE FOR A VALID RESOURCE ID"

publish_iteration_name = "classifyModel"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
# Create a new project
print ("Creating project...")
project = trainer.create_project("Security Project")

authorizedPeopleDir = "C:/python/AzureCognitiveServices/imgs/"
arrAuthorizedPeopleDir = os.listdir(authorizedPeopleDir)

for any in arrAuthorizedPeopleDir:
    urlDir = authorizedPeopleDir + any + "/"
    arrAuth = os.listdir(urlDir)
    tagAuth = trainer.create_tag(project.id, any)
    for path in arrAuth:
        uttt = urlDir + path + "/"
            
        base_image_url_authorized = uttt
        print("Adding " + path + " images...")
        image_list = []
        arrAuthorizedDir = os.listdir(base_image_url_authorized)
        tagName = trainer.create_tag(project.id, path)

        for i in arrAuthorizedDir:
            file_name = i.format()
            with open(base_image_url_authorized  + file_name, "rb") as image_contents:
                image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[tagName.id,tagAuth.id]))
        upload_result = trainer.create_images_from_files(project.id, images=image_list)
        if not upload_result.is_batch_successful:
            print("Image batch upload failed.")
            for image in upload_result.images:
                print("Image status: ", image.status)
            exit(-1)

print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    time.sleep(1)

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")
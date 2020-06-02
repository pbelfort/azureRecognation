import os, shutil
import requests
import time
opc = 0

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"
LOCAL_PATH = 'C:/python/AzureCognitiveServices/testimages/people/'
# Replace with a valid key
training_key = "REPLACE FOR A VALID TRAINING KEY"
#Change prediction_key for Prediction URL <Image> recently created
prediction_key = "REPLACE FOR A VALID PREDICTION KEY"

while True:
    if(opc < 0):
        break;
    while True:
        arr = os.listdir(LOCAL_PATH)
        time.sleep(2)
        if (len(arr) > 0 ):
            break
        print("O diretório " + LOCAL_PATH + " esta vazio!")       
    for any in arr:
        arq = open(LOCAL_PATH + any, 'rb')
        file_path = os.path.join(LOCAL_PATH, any)
        print('Enviando imagem ' + any + ' para API')
        headers = {'Content-Type': 'application/octet-stream','Prediction-Key': training_key}
        url_api = prediction_key
        r_api = requests.post(url_api, data = arq, headers = headers)
        r_api = r_api.json()
        predictor = r_api['predictions'][0]['probability']
        probability = float(predictor)
        print ("Probability: " + str(probability))
        resp =  r_api['predictions'][0]['tagName']
        print (resp)
        arq.close()
        #caso desejar excluir os arquivos da pasta people/
        #os.unlink(file_path) 
    opc = int(input('0 - Executar novamente.\n -1 - Sair:'))
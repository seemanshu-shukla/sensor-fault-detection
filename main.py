from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, File, UploadFile
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd

from fastapi import Request

##Will not be requiring the below part since I have saved the mongodb url in .env file
# env_file_path=os.path.join(os.getcwd(),"env.yaml")

# def set_env_variable(env_file_path):

#     if os.getenv('MONGO_DB_URL',None) is None:
#         env_config = read_yaml_file(env_file_path)
#         os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline() #Creating object of TrainPipeline class
        if train_pipeline.is_pipeline_running: #we will enter this if block if .is_pipeline_running is set to True
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline() #Else when /train route is triggered then start the training pipeline
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        #get data from user csv file
        #conver csv file to dataframe
        df = pd.read_csv(file.file)

        #train df
        #upload df

        #calculate datadrift then trigger an email to the Data Scientist team informing about the same. Also, internally
        #in our training pipline we have configured the data drift based training

        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df) #Before using trained model object we would need to basically use preprocessor model object to preprocess the data shared by user in real time
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True) #getting the original format to target back while sending to the user
        return df.to_html()  #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        # set_env_variable(env_file_path)
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()   #uncomment this line when we want to trigger the training pipline manually using terminal
    # # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)

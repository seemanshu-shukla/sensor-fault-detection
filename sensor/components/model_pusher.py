
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import ModelPusherArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
import os,sys
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.utils.main_utils import save_object,load_object,write_yaml_file

import shutil  #To basically copy file from one file location to other file location

class ModelPusher:

    def __init__(self,
                model_pusher_config:ModelPusherConfig,
                model_eval_artifact:ModelEvaluationArtifact):

        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
        except  Exception as e:
            raise SensorException(e, sys)
    

    def initiate_model_pusher(self,)->ModelPusherArtifact:  #Master Method
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path #representing the newly trained model that needs to be pushed to SAVE_MODEL_DIR where other best performing base models are stored
            
            #Creating model pusher dir to save model --> Location 1 == This is in under "artifact" folder in root dir
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            #saved model dir --> Location 2 == This is in under "saved_models" folder in root dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            return model_pusher_artifact
        except  Exception as e:
            raise SensorException(e, sys)
    
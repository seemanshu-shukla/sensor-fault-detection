
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import ModelEvaluationConfig
import os,sys
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object,write_yaml_file
from sensor.ml.model.estimator import ModelResolver
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping
import pandas  as  pd
class ModelEvaluation:


    def __init__(self,model_eval_config:ModelEvaluationConfig,
                    data_validation_artifact:DataValidationArtifact,
                    model_trainer_artifact:ModelTrainerArtifact):
        
        try:
            self.model_eval_config=model_eval_config
            self.data_validation_artifact=data_validation_artifact
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
    


    def initiate_model_evaluation(self)->ModelEvaluationArtifact:   #Master Method
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            #valid train and test file dataframe
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df,test_df])
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(),inplace=True)
            df.drop(TARGET_COLUMN,axis=1,inplace=True)

            train_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()
            is_model_accepted=True


            if not model_resolver.is_model_exists(): #Representing the case when there is no model available that is the pipeline is running for the first time. In this case we won't be having any base model to perform the comparison. Therefore, we need to accept this model and in subsequent run this will be treated as base model and will get replaced in case new trained model is having better accuracy(ie; 2% more)
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=None, #Since no comparision is made due to unavailablity of the base model
                    best_model_path=None,  #best_model_path will come into picture when there is some kind of comparisons made b/w models. Since in this case it is missing best_model_path=None  
                    trained_model_path=train_model_file_path, #Since this case represents the first run therefore, trained_model_path is set to the model path obtained or stored in ModelTrainerArtifact
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact, #for our trained model metrices were genereate using test split
                    best_model_metric_artifact=None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact

            ## Below represents the case when a valid base model is already available using which we can perform comparison with the newly trained model
            latest_model_path = model_resolver.get_best_model_path() #base model
            latest_model = load_object(file_path=latest_model_path)  #loading the .pkl file for base model
            train_model = load_object(file_path=train_model_file_path)  ##loading the .pkl file for newly trained model
            
            #Now we are starting the comparison process b/w base and newly trained model
            y_trained_pred = train_model.predict(df)  #on top of entire dataset(both test and train dataset from DataValidationArtifact)
            y_latest_pred  =latest_model.predict(df)

            trained_metric = get_classification_score(y_true, y_trained_pred)
            latest_metric = get_classification_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.f1_score-latest_metric.f1_score
            if self.model_eval_config.change_threshold < improved_accuracy:
                #0.02 < 0.03
                is_model_accepted=True
            else:
                is_model_accepted=False

            
            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=improved_accuracy, 
                    best_model_path=latest_model_path, #best base model with whom comparison was made
                    trained_model_path=train_model_file_path, 
                    train_model_metric_artifact=trained_metric, 
                    best_model_metric_artifact=latest_metric)

            ## Now since this trained model accepted in the next stage(model pusher) we will push it inside model_dir
            ## with the latest timestamp. When we are going to train the model again then when we do max(timestamp) then this accepted model will act as a base model

            model_eval_report = model_evaluation_artifact.__dict__

            #save the report
            write_yaml_file(self.model_eval_config.report_file_path, model_eval_report)
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise SensorException(e,sys)

    
    


from credit_card_defaulter.exception import CreditCardDefaulterException
from credit_card_defaulter.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from credit_card_defaulter.config.configuration import DataValidationConfig
from credit_card_defaulter.logger import logging
import os,sys
import pandas  as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

class DataValidation:

    def __init__(self, data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)



    def get_train_and_test_df(self):
        '''
        This function is for starting vaidation
        '''
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)



    def is_train_test_file_exists(self)->bool:
        '''
        This function is for starting vaidation
        '''
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists?-> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)



    def validate_dataset_schema(self)->bool:
        '''
        This function is for starting vaidation
        '''
        try:
            validation_status = False
            
            # Do Required Validation

            validation_status = True
            return validation_status 
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)

    def get_and_save_data_drift_report(self):
        '''
        This function is for starting vaidation
        '''
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())
            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)


    def save_data_drift_report_page(self):
        '''
        This function is for save data drift report page
        '''
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            from credit_card_defaulter.config.configuration import Configuration
            config_obj = Configuration()
            self.data_validation_config = config_obj.get_data_validation_config()
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)


    def is_data_drift_found(self)->bool:
        '''
        This function is for starting vaidation
        '''
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:
        '''
        This function is for starting vaidation
        '''
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact = DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path, report_file_path=self.data_validation_config.report_file_path,
                                                                report_page_file_path=self.data_validation_config.report_page_file_path,
                                                                is_validated=True, message="Data Validation performed successully.")
            return data_validation_artifact
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)


    def __del__(self):
        logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")
       
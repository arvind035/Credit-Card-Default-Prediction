from credit_card_defaulter.entity.artifact_entity import DataIngestionArtifact
from credit_card_defaulter.entity.config_entity import DataIngestionConfig
import shutil, os, sys, zipfile
from credit_card_defaulter.exception import CreditCardDefaulterException
from credit_card_defaulter.constant import *
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split




class DataIngestion:

    def __init__(self, data_ingestion_config=DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)


    def load_data(self) ->str:
        '''
        This function for loadind data for storage
        '''
        try:
            data_url = self.data_ingestion_config.dataset_url
            tgz_dir = self.data_ingestion_config.tgz_dir
            os.makedirs(tgz_dir, exist_ok = True)
            file_name = os.path.basename(data_url)
            tgz_file_path = os.path.join(tgz_dir, file_name)
            shutil.copy(str(data_url), str(tgz_file_path))
            return tgz_file_path
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)

    def extract_tgz_file(self, tgz_file_path:str):
        '''
        This function for extrcating data from zip
        '''
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir,exist_ok=True)
            with zipfile.ZipFile(tgz_file_path, 'r') as zip:
                zip.extractall(raw_data_dir)
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)

    def split_data_into_train_test(self) ->DataIngestionArtifact:
        '''
        This function for spliting data into train and test
        '''
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            ingested_train_dir = self.data_ingestion_config.ingested_train_dir
            ingested_test_dir = self.data_ingestion_config.ingested_test_dir
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]
            fetch_url = os.path.join(raw_data_dir, file_name)
            data = pd.read_csv(fetch_url)
            
            train_dataset = []
            test_dataset = []
            train_dataset, test_dataset = train_test_split(data, test_size=0.2, random_state=42)

            train_file_path = os.path.join(ingested_train_dir, file_name)
            test_file_path = os.path.join(ingested_test_dir, file_name)

            if train_dataset is not None:
                os.makedirs(ingested_train_dir, exist_ok=True)
                train_dataset.to_csv(train_file_path, index = False)

            if test_dataset is not None:
                os.makedirs(ingested_test_dir, exist_ok=True)
                test_dataset.to_csv(test_file_path, index = False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path, test_file_path=test_file_path,
                                                            is_ingested=True, message="Data ingestion completed successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)

    def initiate_data_ingestion(self):
        '''
        This function for initiate data ingestion
        '''
        try:
            tgz_file_path = self.load_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_into_train_test()
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)    

    def __del__(self):
        pass
import os
import sys

from credit_card_defaulter.exception import CreditCardDefaulterException
from credit_card_defaulter.util.util import load_object

import pandas as pd


class CcDefaultData:

    def __init__(self,
                    LIMIT_BAL: int,
                    SEX: int,
                    EDUCATION: int,
                    MARRIAGE: int,
                    AGE: int,
                    PAY_0: int,
                    PAY_2: int,
                    PAY_3: int,
                    PAY_4: int,
                    PAY_5: int,
                    PAY_6: int,
                    BILL_AMT1: int,
                    BILL_AMT2: int,
                    BILL_AMT3: int,
                    BILL_AMT4: int,
                    BILL_AMT5: int,
                    BILL_AMT6: int,
                    PAY_AMT1: int,
                    PAY_AMT2: int,
                    PAY_AMT3: int,
                    PAY_AMT4: int,
                    PAY_AMT5: int,
                    PAY_AMT6: int
                 ):
        try:
            self.LIMIT_BAL=LIMIT_BAL
            self.SEX=SEX
            self.EDUCATION=EDUCATION
            self.MARRIAGE=MARRIAGE
            self.AGE=AGE
            self.PAY_0=PAY_0
            self.PAY_2=PAY_2
            self.PAY_3=PAY_3
            self.PAY_4=PAY_4
            self.PAY_5=PAY_5
            self.PAY_6=PAY_6
            self.BILL_AMT1=BILL_AMT1
            self.BILL_AMT2=BILL_AMT2
            self.BILL_AMT3=BILL_AMT3
            self.BILL_AMT4=BILL_AMT4
            self.BILL_AMT5=BILL_AMT5
            self.BILL_AMT6=BILL_AMT6
            self.PAY_AMT1=PAY_AMT1
            self.PAY_AMT2=PAY_AMT2
            self.PAY_AMT3=PAY_AMT3
            self.PAY_AMT4=PAY_AMT4
            self.PAY_AMT5=PAY_AMT5
            self.PAY_AMT6=PAY_AMT6
        except Exception as e:
            raise CreditCardDefaulterException(e, sys) from e

    def get_ccDefault_input_data_frame(self):

        try:
            ccd_input_dict = self.get_ccDefault_data_as_dict()
            return pd.DataFrame(ccd_input_dict)
        except Exception as e:
            raise CreditCardDefaulterException(e, sys) from e

    def get_ccDefault_data_as_dict(self):
        try:
            input_data = {'LIMIT_BAL': [self.LIMIT_BAL],
                            'SEX': [self.SEX],
                            'EDUCATION': [self.EDUCATION],
                            'MARRIAGE': [self.MARRIAGE],
                            'AGE': [self.AGE],
                            'PAY_0': [self.PAY_0],
                            'PAY_2': [self.PAY_2],
                            'PAY_3': [self.PAY_3],
                            'PAY_4': [self.PAY_4],
                            'PAY_5': [self.PAY_5],
                            'PAY_6': [self.PAY_6],
                            'BILL_AMT1': [self.BILL_AMT1],
                            'BILL_AMT2': [self.BILL_AMT2],
                            'BILL_AMT3': [self.BILL_AMT3],
                            'BILL_AMT4': [self.BILL_AMT4],
                            'BILL_AMT5': [self.BILL_AMT5],
                            'BILL_AMT6': [self.BILL_AMT6],
                            'PAY_AMT1': [self.PAY_AMT1],
                            'PAY_AMT2': [self.PAY_AMT2],
                            'PAY_AMT3': [self.PAY_AMT3],
                            'PAY_AMT4': [self.PAY_AMT4],
                            'PAY_AMT5': [self.PAY_AMT5],
                            'PAY_AMT6': [self.PAY_AMT6]
                }
            return input_data
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)


class CcDefaultPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise CreditCardDefaulterException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise CreditCardDefaulterException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            ccd_value = model.predict(X)
            return ccd_value
        except Exception as e:
            raise CreditCardDefaulterException(e, sys)   
from flask import Flask
from credit_card_defaulter.config.configuration import Configuration
from credit_card_defaulter.component.data_ingestion import DataIngestion
from credit_card_defaulter.pipeline.pipeline import Pipeline
from credit_card_defaulter.constant import *

app = Flask(__name__)


def main():
        pipeline = Pipeline(Configuration())
        pipeline.initiate_model_training()    



if __name__ == "__main__":
    main()
#     app.run(debug=True)
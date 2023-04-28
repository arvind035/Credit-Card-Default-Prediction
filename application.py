from flask import Flask, redirect, url_for, render_template, request, flash
from credit_card_defaulter.config.configuration import Configuration
from credit_card_defaulter.component.data_ingestion import DataIngestion
from credit_card_defaulter.pipeline.pipeline import Pipeline
from credit_card_defaulter.constant import *
from credit_card_defaulter.entity.cc_defaultor_predictor import CcDefaultData, CcDefaultPredictor


ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "credit_card_defaulter"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


app = Flask(__name__)
@app.route('/')
def home():
        return render_template('index.html')

@app.route('/prediction', methods=['GET','POST'])
def predict():
        if request.method == 'GET':
                return render_template('home.html')
        if request.method == 'POST':
                ccd_data = CcDefaultData(LIMIT_BAL=int(request.form.get('LIMIT_BAL')),
                                                SEX=int(request.form.get('SEX')),
                                                EDUCATION=int(request.form.get('EDUCATION')),
                                                MARRIAGE=int(request.form.get('MARRIAGE')),
                                                AGE=int(request.form.get('AGE')),
                                                PAY_0=int(request.form.get('PAY_0')),
                                                PAY_2=int(request.form.get('PAY_2')),
                                                PAY_3=int(request.form.get('PAY_3')),
                                                PAY_4=int(request.form.get('PAY_4')),
                                                PAY_5=int(request.form.get('PAY_5')),
                                                PAY_6=int(request.form.get('PAY_6')),
                                                BILL_AMT1=int(request.form.get('BILL_AMT1')),
                                                BILL_AMT2=int(request.form.get('BILL_AMT2')),
                                                BILL_AMT3=int(request.form.get('BILL_AMT3')),
                                                BILL_AMT4=int(request.form.get('BILL_AMT4')),
                                                BILL_AMT5=int(request.form.get('BILL_AMT5')),
                                                BILL_AMT6=int(request.form.get('BILL_AMT6')),
                                                PAY_AMT1=int(request.form.get('PAY_AMT1')),
                                                PAY_AMT2=int(request.form.get('PAY_AMT2')),
                                                PAY_AMT3=int(request.form.get('PAY_AMT3')),
                                                PAY_AMT4=int(request.form.get('PAY_AMT4')),
                                                PAY_AMT5=int(request.form.get('PAY_AMT5')),
                                                PAY_AMT6=int(request.form.get('PAY_AMT6'))
                                                )
                data = ccd_data.get_ccDefault_input_data_frame()
                ccd_predictor = CcDefaultPredictor(model_dir=MODEL_DIR)
                ccd_value = ccd_predictor.predict(X=data)
                return render_template('home.html', data=ccd_value[0])
 
@app.route('/training', methods=['GET'])
def training():
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        #pipeline.run_pipeline()
        pipeline.start()   


if __name__ == "__main__":
    app.run(debug=True)
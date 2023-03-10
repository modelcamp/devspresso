import json
import inferences_service
import os
import session_manager
from constants import INFERENCE_VALUE_RESPONSE_KEY, INFERENCE_LANGUAGE_RESPONSE_KEY, OPENAI_KEY_PARAM_NAME, OPENAI_ORGANIZATION_ID_PARAM_NAME
from chat_helpers import CodeInferenceResult
from dotenv import load_dotenv
from inference_models import inference_model
from flask import Flask, request, Response, render_template

app = Flask(__name__)
load_dotenv()

# Configure environment keys.
app.secret_key = os.getenv("FLASK_SESSION_KEY")

@app.route("/")
def index():
    # When home page is loaded, clear previous context to establish a new conversation.
    session_manager.clear_all_model_contexts()
    openai_key: str = session_manager.get_openai_key()
    openai_organization_id: str = session_manager.get_openai_organization_id()
    return render_template(
        'index.html',
        inference_prompt_name=inference_model.InferenceModel.inference_prompt_name,
        inference_value_response_key=INFERENCE_VALUE_RESPONSE_KEY,
        inference_language_response_key=INFERENCE_LANGUAGE_RESPONSE_KEY,
        openai_key_param_name=OPENAI_KEY_PARAM_NAME,
        openai_organization_id_param_name=OPENAI_ORGANIZATION_ID_PARAM_NAME,
        openai_key_prefill_value=openai_key,
        openai_organization_id_prefill_value=openai_organization_id)

@app.route("/contact")
def contact():
    return render_template(
        'contact.html')

@app.route("/infer", methods=['POST'])
def infer():
    inference_input: str = request.args[inference_model.InferenceModel.inference_prompt_name]
    openai_api_key: str = request.args[OPENAI_KEY_PARAM_NAME]
    openai_organization_id: str = request.args[OPENAI_ORGANIZATION_ID_PARAM_NAME]

    inference: CodeInferenceResult = inferences_service.infer(
        json.loads(inference_input),
        openai_api_key,
        openai_organization_id)
    response = Response(
        response=json.dumps({
            INFERENCE_VALUE_RESPONSE_KEY: inference.value,
            INFERENCE_LANGUAGE_RESPONSE_KEY: inference.language
        }),
        content_type='application/json')

    return response

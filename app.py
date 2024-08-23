from flask import Flask, render_template, request
import webscraping_ai
from webscraping_ai.rest import ApiException
from pprint import pprint

app = Flask(__name__)

# Webscraping.ai API Configuration
configuration = webscraping_ai.Configuration(
    host="https://api.webscraping.ai"
)

# Set up API key authorization
configuration.api_key['api_key'] = '1af2fb38-9945-4fcc-aae6-c4377bf0211f'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    url = request.form['url']
    question = request.form['question']

    # Enter a context with an instance of the API client
    with webscraping_ai.ApiClient(configuration) as api_client:
        api_instance = webscraping_ai.AIApi(api_client)
        context_limit = 4000
        response_tokens = 100
        on_context_limit = 'error'
        headers = {'key': '{\"Cookie\":\"session=some_id\"}'}
        timeout = 10000
        js = True
        js_timeout = 2000
        proxy = 'datacenter'
        country = 'us'
        device = 'desktop'
        error_on_404 = False
        error_on_redirect = False
        js_script = "document.querySelector('button').click();"

        try:
            # Get an answer to a question about a given web page
            api_response = api_instance.get_question(
                url, question=question, context_limit=context_limit, 
                response_tokens=response_tokens, on_context_limit=on_context_limit, 
                headers=headers, timeout=timeout, js=js, js_timeout=js_timeout, 
                proxy=proxy, country=country, device=device, 
                error_on_404=error_on_404, error_on_redirect=error_on_redirect, 
                js_script=js_script
            )

            # Print the response to check its structure
            print("API Response:", api_response)

            # Handle the response based on its type
            if isinstance(api_response, dict):
                # If it's a dictionary, get the 'answer' key
                result = api_response.get('answer', 'No answer found in the response.')
            elif isinstance(api_response, str):
                # If it's a string, use it as-is
                result = api_response
            else:
                # Fallback in case of an unexpected type
                result = "Unexpected response type received from the API."

        except ApiException as e:
            result = f"Exception when calling AIApi->get_question: {e}"

    return render_template('result.html', url=url, question=question, result=result)

if __name__ == '__main__':
    app.run(debug=True)

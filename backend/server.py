import requests
from secret import wavekey
from openai import OpenAI
from flask import Flask, request
import datetime
import json
from flask_cors import CORS  # Import CORS

# Initializing flask app with CORS
app = Flask(__name__)
CORS(app)

client = OpenAI()
webisteURL = 'https://pages.cs.wisc.edu/~oliphant/cs537-sp24/'

def get_wave_analysis(url):
    # wave_url = 'https://wave.webaim.org/api/request?key=' + wavekey + '&reporttype=2&url=' + url
    # wave_request = requests.get(wave_url)
    # wave_analysis = wave_request.text
    # print(wave_analysis)
    
    # hardcode for testing
    wave_analysis = '''{"status":{"success":true,"httpstatuscode":200},"statistics":{"pagetitle":"Google","pageurl":"google.com","time":3.22,"creditsremaining":49,"allitemcount":140,"totalelements":367,"waveurl":"http://wave.webaim.org/report?url=google.com"},"categories":{"error":{"description":"Errors","count":1,"items":{"label_missing":{"id":"label_missing","description":"Missing form label","count":1}}},"contrast":{"description":"Contrast Errors","count":0,"items":[]},"alert":{"description":"Alerts","count":2,"items":{"heading_missing":{"id":"heading_missing","description":"No heading structure","count":1},"text_small":{"id":"text_small","description":"Very small text","count":1}}},"feature":{"description":"Features","count":12,"items":{"alt":{"id":"alt","description":"Alternative text","count":1},"alt_null":{"id":"alt_null","description":"Null or empty alternative text","count":10},"lang":{"id":"lang","description":"Language","count":1}}},"structure":{"description":"Structural Elements","count":5,"items":{"ul":{"id":"ul","description":"Unordered list","count":1},"iframe":{"id":"iframe","description":"Inline frame","count":1},"nav":{"id":"nav","description":"Navigation","count":1},"search":{"id":"search","description":"Search","count":1},"footer":{"id":"footer","description":"Footer","count":1}}},"aria":{"description":"ARIA","count":120,"items":{"aria":{"id":"aria","description":"ARIA","count":59},"aria_label":{"id":"aria_label","description":"ARIA label","count":15},"aria_tabindex":{"id":"aria_tabindex","description":"ARIA tabindex","count":20},"aria_menu":{"id":"aria_menu","description":"ARIA menu","count":1},"aria_button":{"id":"aria_button","description":"ARIA button","count":16},"aria_hidden":{"id":"aria_hidden","description":"ARIA hidden","count":3},"aria_expanded":{"id":"aria_expanded","description":"ARIA expanded","count":3},"aria_haspopup":{"id":"aria_haspopup","description":"ARIA popup","count":3}}}}}'''
    return wave_analysis

def get_openai_report(wave_analysis):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": """You are a meticulous web accessibility professional, conducting a thorough analysis of a website's accessibility using the WAVE tool. As a web accessibility professional and expert, your task is to analyze the accessibility of the website using the WAVE (Web Accessibility Evaluation) tool and provide helpful advice on changes to make the site more accessible. Additionally, offer a detailed explanation of the issues found by WAVE. Lastly, give a rating of the accessibility of the site out of 10. Give the report in this JSON format report: {
      summary: "",
      errors: {},
      alerts: {},
      features: {},
      rating: 0,
    }."""},
            {"role": "user", "content": wave_analysis}
        ]
    )
    
    # Check if completion.choices is not empty
    if completion.choices:
        openai_report = completion.choices[0].message.content
        return openai_report
    else:
        return '{"summary": "Unable to generate OpenAI report"}'



def report(url):
    x = datetime.datetime.now()
    wave_analysis = get_wave_analysis(url)
    openai_report = get_openai_report(wave_analysis)
    #convert str to json
    openai_report = json.loads(openai_report)

    # Log the received data for debugging
    print("OpenAI Report:", openai_report)

    # Ensure the response structure matches the frontend expectation
    response = {
        "Date": x.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "summary": openai_report.get("summary", {}),
        "errors": openai_report.get("errors", {}),
        "alerts": openai_report.get("alerts", {}),
        "features": openai_report.get("features", {}),
        "rating": openai_report.get("rating", 0),
    }

    return response




@app.route('/report', methods=['GET'])
def get_report():
    url = request.args.get('url')

    if not url:
        return {"error": "URL parameter is missing"}, 400

    response = report(url)
    return response

# Removing unreachable code from the main function
# Running app
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS

import requests
from  bs4 import BeautifulSoup
import js2xml

app = Flask(__name__)
CORS(app)

# main functions =======================================================

# target_keywords
heatMarker_wrap_property = "heatMarkerRenderer"
heatMarker_score_property = "heatMarkerIntensityScoreNormalized"
heatMarker_timeRange_property = "timeRangeStartMillis"

# Youtubeからtarget_keywordが含まれるscriptタグを取得
def get_script_tag(youtube_link):
    responce = requests.get(youtube_link)
    if responce.status_code == 200:
        html_content = responce.text
        soup = BeautifulSoup(html_content, 'html.parser')
        scripts = soup.find_all('script')
        target_script = None
        for script in scripts:
            if heatMarker_wrap_property in script.text:
                target_script = script
                break
    if target_script:
        data = target_script.text
    
    return(data)

# target_keywordのvalueを読み取る
def get_property_values(script_tag):
    parsed_js = js2xml.parse(script_tag)

    for prop in parsed_js.xpath(f'//property[@name="{heatMarker_wrap_property}"]'):
        start_time = prop.xpath(f'.//property[@name="{heatMarker_timeRange_property}"]/number/@value')[0]
        score = prop.xpath(f'.//property[@name="{heatMarker_score_property}"]/number/@value')[0]
        if score == "1":
            break
    
    return start_time

def generate_youtube_url(start_time_ms, youtube_link):
    result = ""

    start_time_s = int(start_time_ms) / 1000

    result = youtube_link + "&t=" + str(start_time_s) + "s"

    return result

# ======================================================================

@app.route("/")
def hello():
    hello_api = {
        "Name" : "Busyoutbe backend",
    }
    return jsonify(hello_api)

@app.route('/process_youtube_link', methods=['POST'])
def process_youtube_link():
    try:
        # POSTリクエストからJSONデータを受け取る
        data = request.get_json()
        # YouTubeのリンクを取得
        youtube_link = data.get('youtube_link')

        script_tag = get_script_tag(youtube_link)
        start_time = get_property_values(script_tag)
        url = generate_youtube_url(start_time, youtube_link)

        return(url)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

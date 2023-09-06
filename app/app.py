from flask import Flask, jsonify, request

import requests
from  bs4 import BeautifulSoup
import js2xml

app = Flask(__name__)

# main functions =======================================================

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
    result = []

    for prop in parsed_js.xpath(f'//property[@name="{heatMarker_wrap_property}"]'):
        property_values = []
        start_time = prop.xpath(f'.//property[@name="{heatMarker_timeRange_property}"]/number/@value')[0]
        score = prop.xpath(f'.//property[@name="{heatMarker_score_property}"]/number/@value')[0]
        property_values.append(start_time)
        property_values.append(score)

        result.append(f"start_time: {start_time}, score: {score}")
        # result.append(score)

    return result

# script_tagからtarget_keywordが含まれる配列を取り出す
def get_objectArrays(script_tag):

    property_values_array = []

    property_values = get_property_values(script_tag)

    if property_values:
        for value in property_values:
            property_values_array.append(value)
    
    result = "\n".join(property_values_array)

    return(result)


# main functions =======================================================

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
        objectArrays_in_script_tag = get_objectArrays(script_tag)

        return(objectArrays_in_script_tag)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

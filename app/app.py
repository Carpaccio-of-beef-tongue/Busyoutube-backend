from flask import Flask, jsonify, request
import requests
from  bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def hello():
    hello_api = {
        "Name" : "Busyoutbe backend",
    }
    return jsonify(hello_api)

# main
@app.route('/process_youtube_link', methods=['POST'])
def process_youtube_link():
    try:
        # POSTリクエストからJSONデータを受け取る
        data = request.get_json()

        # YouTubeのリンクを取得
        youtube_link = data.get('youtube_link')

        # YouTubeのリンクを処理することができます
        responce = requests.get(youtube_link)
        if responce.status_code == 200:
            html_content = responce.text
            soup = BeautifulSoup(html_content, 'html.parser')
            scripts = soup.find_all('script')
            target_script = None

            for script in scripts:
                if 'heatMarkerIntensityScoreNormalized' in script.text:
                    target_script = script
                    break

        if target_script:
            data = target_script.text
        
        

        # この例では、単にリンクを返しますが、実際の処理を追加できます

        # return jsonify({'message': 'YouTube link received and processed successfully.'})
        return(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

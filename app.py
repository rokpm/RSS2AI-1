from flask import Flask, render_template, request, jsonify, send_from_directory
import rss
import uuid
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_feed():
    try:
        original_feed = request.form.get('rss_feed')
        if not original_feed:
            return jsonify(error="缺少 RSS 订阅源参数"), 400
        print(f"接收到的 RSS 订阅源: {original_feed}")
        new_feed = rss.generate_summary_feed(original_feed)
        filename = str(uuid.uuid4()) + ".xml"
        rss.save_feed_to_file(new_feed, filename)
        feed_url = request.url_root + "feeds/" + filename
        print(f"生成的新 RSS 订阅源 URL: {feed_url}")
        return jsonify(new_feed=feed_url)
    except Exception as e:
        print(f"生成 RSS 订阅源时出错: {str(e)}")
        return jsonify(error="生成新的 RSS 订阅源时出错，请稍后重试。"), 500

@app.route('/feeds/<path:filename>')
def send_feed_file(filename):
    return send_from_directory('feeds', filename)

if __name__ == '__main__':
    app.run(debug=True)
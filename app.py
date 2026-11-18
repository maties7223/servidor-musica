from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download_audio():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Falta la URL"}), 400

    file_id = str(uuid.uuid4())
    output_template = f"/tmp/{file_id}.%(ext)s"

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': output_template,
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'cancion')

        return send_file(
            filename,
            as_attachment=True,
            download_name=f"{title}.m4a",
            mimetype="audio/mp4"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
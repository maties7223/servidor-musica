from flask import Flask, request, send_file
import yt_dlp
import os
import base64

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_audio():
    video_url = request.args.get('url')
    if not video_url:
        return "Falta el parámetro 'url'", 400

    os.makedirs('downloads', exist_ok=True)

    cookie_path = 'cookies.txt'
    cookies_b64 = os.getenv('YOUTUBE_COOKIES_BASE64')
    if cookies_b64:
        try:
            decoded_bytes = base64.b64decode(cookies_b64)
            with open(cookie_path, 'wb') as f:
                f.write(decoded_bytes)
        except Exception as e:
            print(f"Error decodificando cookies: {e}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        },
        'socket_timeout': 30
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            final_file = base + ".m4a"

        return send_file(final_file, as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Render asigna un puerto dinámico mediante la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

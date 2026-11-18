from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_audio():
    video_url = request.args.get('url')
    if not video_url:
        return "Falta el parámetro 'url'", 400

    # Carpeta temporal para guardar el audio
    os.makedirs('downloads', exist_ok=True)
    
    # Configuración de yt-dlp con camuflaje de navegador para evitar bloqueos
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            # Cambiamos la extensión a .m4a que es el resultado final del postprocessor
            base, _ = os.path.splitext(filename)
            final_file = base + ".m4a"

        return send_file(final_file, as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

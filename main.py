#https://aws.amazon.com/fr/getting-started/hands-on/serve-a-flask-app/

from io import BytesIO
from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return render_template("/index.html",
                            mytitle="ytb2mp4",
                            mydescription="Type a youtube url to download its mp4 version:",
                            myexample="example: https://www.youtube.com/watch?v=iC8oP4Z_xPw"
                           )

@app.route("/", methods = ['post'])
def dwnld_mp4_from_ytb_url():
    link = request.form['name']
    only_audio = True if 'only_audio' in request.form.keys() else False
    stream = YouTube(link).streams.filter(file_extension='mp4', only_audio=only_audio)[0]
    filename = stream.default_filename
    buffer = BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        attachment_filename=filename,
        mimetype= "audio/mp4" if only_audio else "video/mp4",
    )


if __name__ == "__main__":
   app.run(debug=True)
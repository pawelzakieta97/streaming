import json

from flask import Flask, render_template, redirect, url_for, request

import os

app = Flask('name', static_folder='static', template_folder='templates')

root_dir = 'static'
LAST_WATCHED_FILENAME = 'last_watched.txt'
VIDEO_EXTENSIONS = ['.mp4', '.mkv']

@app.route('/browse/')
@app.route('/browse/<path:path>')
def browse(path='.'):
    parent = os.path.split(path)[0]
    if not parent:
        parent = '.'
    elements = os.listdir(os.path.join(root_dir, path))
    elements = sorted(elements)
    files = [e for e in elements if os.path.isfile(os.path.join(root_dir, path, e))]
    directories = [e for e in elements if e not in files]

    last_watched = None
    if os.path.exists(LAST_WATCHED_FILENAME):
        with open(LAST_WATCHED_FILENAME) as f:
            last_watched = f.read()

    return render_template('browse2.html', path=path, files=files, parent=parent,
                           directories=directories, last_watched=last_watched)


@app.route('/')
def home():
    return redirect(url_for('browse'))

@app.route('/watch/<path:video_file>')
def watch(video_file):
    fullscreen = request.args.get('fullscreen')
    file_directory, file_name = os.path.split(video_file)
    files = os.listdir(os.path.join(root_dir, file_directory))
    files = filter(lambda filename: any([filename.endswith(ext) for ext in VIDEO_EXTENSIONS]), files)
    files = sorted(files)
    files = [f for f in files if os.path.isfile(os.path.join(root_dir, file_directory, f))]
    video_file_index = files.index(file_name)
    previous_file = files[video_file_index - 1] if video_file_index >= 1 else None
    next_file = files[video_file_index + 1] if video_file_index < len(files) - 1 else None
    with open(LAST_WATCHED_FILENAME, 'w+') as f:
        f.write(video_file)
    return render_template('watch.html', filename=video_file,
                           previous_file=previous_file,
                           next_file=next_file,
                           directory=file_directory,
                           fullscreen=fullscreen,
                           files=json.dumps(files),
                           current_file_index=video_file_index)

@app.route('/last_watched/<path:video_file>', methods=['POST'])
def update_last_watched(video_file):
    with open(LAST_WATCHED_FILENAME, 'w+') as f:
        f.write(video_file)
    return video_file

if __name__ == '__main__':
    app.run("0.0.0.0")
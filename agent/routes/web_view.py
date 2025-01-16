from . import *

@app.route('/')
@login_required
def home():
    css_files = [f for f in os.listdir(f'{app_workdir}/templates/css') if f.endswith('.css')]
    js_files = [f for f in os.listdir(f'{app_workdir}/templates/js') if f.endswith('.js')]
    return render_template('index.html', user=current_user.username, user_id=current_user.id, css_files=css_files, js_files=js_files)

@app.route('/css/<filename>')
@login_required
def serve_style(filename):
    # Sanitize the filename to prevent directory traversal attacks
    safe_filename = os.path.basename(filename)

    # Check if the file exists in the directory
    file_path = os.path.join(f'{app_workdir}/templates/css', safe_filename)
    if not os.path.isfile(file_path):
        abort(404)

    # Serve the file
    return send_from_directory(f'{app_workdir}/templates/css', safe_filename)


@app.route('/js/<filename>')
@login_required
def serve_javascript(filename):
    # Sanitize the filename to prevent directory traversal attacks
    safe_filename = os.path.basename(filename)

    # Check if the file exists in the directory
    file_path = os.path.join(f'{app_workdir}/templates/js', safe_filename)
    if not os.path.isfile(file_path):
        abort(404)

    # Serve the file
    return send_from_directory(f'{app_workdir}/templates/js', safe_filename)


@app.route('/modal')
@login_required
def modal():
    return render_template('modal.html')

@app.route('/api/modal', methods=['POST'])
@login_required
def get_modal():
    # <@e3>http://example.com
    data = request.json
    title = data.get('title', 'Default Title')
    message = data.get('message', 'Default Message')
    target = data.get('target', 'Default Message')
    modal_html = render_template_string('''
    <div id="myModal" class="modal track-click">
      <div style="height: 700px" class="modal-content">
        <span class="close track-click">x</span>
        <h2>{{ title }}</h2>
        <p>{{ message }}</p>
        <iframe style="width: 100%; height: 700px; class="track-click" src={{ target }}></iframe>
      </div>
    </div>
''', title=title, message=message, target=target)
    print(data)
    return jsonify({'modal_html': modal_html})
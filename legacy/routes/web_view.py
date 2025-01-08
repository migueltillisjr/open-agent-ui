from . import *

@app.route('/')
#@login_required
def home():
    return render_template('index.html', user=current_user.username, user_id=current_user.id)

# Protect the main route
@app.route('/core')
#@login_required
def core():
    return render_template('core.html', user=current_user.username, user_id=current_user.id)

@app.route('/core.styleguide.css')
#@login_required
def core_style_guide():
    return render_template('core.styleguide.css', user=current_user.username, user_id=current_user.id)

@app.route('/chat.css')
#@login_required
def chat_css():
    return send_file(f'{app_workdir}/templates/chat.css')

@app.route('/chat.js')
#@login_required
def chat_js():
    return send_file(f'{app_workdir}/templates/chat.js')

@app.route('/marked.min.js')
#@login_required
def marked_js():
    return send_file(f'{app_workdir}/templates/marked.min.js')

@app.route('/core.style.css')
#@login_required
def core_style():
    return render_template('core.style.css', user=current_user.username, user_id=current_user.id)


@app.route('/modal')
#@login_required
def modal():
    return render_template('modal.html')

@app.route('/api/modal', methods=['POST'])
#@login_required
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

@app.route('/dashboard')
#@login_required
def dashboard():
    return f'Hello, {current_user.username}! Welcome to your dashboard.'
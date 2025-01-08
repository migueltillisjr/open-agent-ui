from . import *


# Combined route for listing, downloading, and deleting archives
@app.route('/bounce_lists', defaults={'filename': None}, methods=['GET', 'POST'])
@app.route('/bounce_lists/<filename>', methods=['GET', 'POST'])
@login_required
def bounce_lists(filename):
    archive_type = "bounce_lists"
    FILE_DIRECTORY = f'{app_workdir}/app-files/users/{current_user.id}/{archive_type}'
    if request.method == 'GET':
        if filename:  # If a filename is specified, serve the file for download
            return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)
        else:  # If no filename, list all files
            files = os.listdir(FILE_DIRECTORY)
            return render_template('files.html', files=files, archive_type=archive_type)

    if request.method == 'POST':
        if filename:  # If a filename is specified, delete the file
            file_path = os.path.join(FILE_DIRECTORY, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for(archive_type))
        return "File not specified", 400


@app.route('/email_lists', defaults={'filename': None}, methods=['GET', 'POST'])
@app.route('/email_lists/<filename>', methods=['GET', 'POST'])
@login_required
def email_lists(filename):
    archive_type = "email_lists"
    FILE_DIRECTORY = f'{app_workdir}/app-files/users/{current_user.id}/{archive_type}'
    if request.method == 'GET':
        if filename:  # If a filename is specified, serve the file for download
            return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)
        else:  # If no filename, list all files
            files = os.listdir(FILE_DIRECTORY)
            return render_template('files.html', files=files, archive_type=archive_type)

    if request.method == 'POST':
        if filename:  # If a filename is specified, delete the file
            file_path = os.path.join(FILE_DIRECTORY, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for(archive_type))
        return "File not specified", 400
    

@app.route('/contacts', defaults={'filename': None}, methods=['GET', 'POST'])
@app.route('/contacts/<filename>', methods=['GET', 'POST'])
@login_required
def contacts(filename):
    archive_type = "contacts"
    FILE_DIRECTORY = f'{app_workdir}/app-files/users/{current_user.id}/{archive_type}'
    if request.method == 'GET':
        if filename:  # If a filename is specified, serve the file for download
            return send_from_directory(FILE_DIRECTORY, filename, as_attachment=True)
        else:  # If no filename, list all files
            files = os.listdir(FILE_DIRECTORY)
            return render_template('files.html', files=files, archive_type=archive_type)

    if request.method == 'POST':
        if filename:  # If a filename is specified, delete the file
            file_path = os.path.join(FILE_DIRECTORY, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for(archive_type))
        return "File not specified", 400  

@app.route('/upload_contacts', methods=['POST'])
@login_required
def upload_contacts():
    try:
        # Check if the 'file' field is in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        # Check if a file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Save the file
        file_path = f'{app_workdir}/app-files/users/{current_user.id}/uploads/user_contacts.csv'
        file.save(file_path)
        
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_campaigns', methods=['POST'])
@login_required
#@require_api_key  # Require API key for this POST route
def delete_campaigns():
    filenames_to_delete=list()
    data = request.json
    delete_campaign_files(data['campaigns'])
    return jsonify({"response": "OK"})


@app.route('/list_campaigns', methods=['GET'])
@login_required
#@require_api_key  # Require API key for this POST route
def list_campaigns():
    filenames=list()
    #data = request.json
    campaign_files = return_campaign_files()
    return jsonify({"response": campaign_files})


@app.route('/query', methods=['POST'])
@login_required
#@require_api_key  # Require API key for this POST route
def post_example():
    data = request.json
    if ('subject' in data.keys()) and ('scheduledAt' in data.keys()):
        adhoc_build_campaign(data)
    return jsonify({"response": "OK"})

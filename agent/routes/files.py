from . import *


# File upload route
@app.route('/chat/<chat_id>/upload-file', methods=['POST'])
@login_required
def upload_file(chat_id):
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    if file:
        # file_name = secure_filename(file.filename)

        file_name = secure_filename('user_contacts.csv')
        file_path = os.path.join(f'{app_workdir}/app-files/users/{current_user.id}/uploads', file_name)
        file.save(file_path)

        # Save the file upload message to the chat history in the database
        message_content = f"File Uploaded: {file_name}"
        new_message = Message(chat_id=chat_id, sender='user', content=message_content)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({'success': True, 'message': message_content}), 200
    return jsonify({'success': False, 'error': 'File upload failed'}), 500






###########################################################################################
# File Management                                                                         #
###########################################################################################

# Route to handle image upload
@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    # Secure the filename and save the image
    filename = secure_filename(image.filename)
    filepath = os.path.join(f'{app_workdir}/app-files/users/{current_user.id}/uploads/imgs/', filename)
    image.save(filepath)

    # Return the image URL to be used in the editor
    image_url = f'/static/uploads/{filename}'

    return jsonify({'url': image_url})

# Route to serve the uploaded images
@app.route('/static/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(f'{app_workdir}/app-files/users/{current_user.id}/uploads/imgs/', filename)

# Route to load pre-existing images
@app.route('/load_images')
@login_required
def load_images():
    image_files = os.listdir(f'{app_workdir}/app-files/users/{current_user.id}/uploads/imgs/')
    image_urls = [f'/static/uploads/{file}' for file in image_files]
    return jsonify({'images': image_urls})



# Route to download or serve a file from the server
@app.route('/imgs/<filename>')
# @login_required
def images(filename):
    return send_from_directory(app.config['IMGS'], filename)

# Route to view all uploaded files
@app.route('/files', methods=['GET'])
@login_required
def list_files():
    files = os.listdir(f'{app_workdir}/app-files/users/{current_user.id}/uploads')
    return jsonify([{"name": file} for file in files])

# Route to download a file
@app.route('/download-file', methods=['GET'])
@login_required
def download_file():
    file_name = request.args.get('filename')
    if file_name and os.path.exists(os.path.join(f'{app_workdir}/app-files/users/{current_user.id}/uploads', file_name)):
        return send_from_directory(f'{app_workdir}/app-files/uploads', file_name, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

# Route to delete a file
@app.route('/delete-file', methods=['DELETE'])
@login_required
def delete_file():
    file_name = request.args.get('filename')
    file_path = os.path.join(f'{app_workdir}/app-files/users/{current_user.id}/uploads', file_name)
    if file_name and os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True}), 200
    return jsonify({"error": "File not found"}), 404

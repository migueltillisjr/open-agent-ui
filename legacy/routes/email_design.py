from . import *


# Helper function to get available templates
# def get_available_templates():
#     # Define the directory where the templates are stored
#     TEMPLATE_DIR = f'{app_workdir}/app-files/users/{current_user.id}/uploads/'  # Store your HTML templates in this directory
#     templates = {}
#     for filename in os.listdir(TEMPLATE_DIR):
#         if filename.endswith('.html'):
#             if filename != 'email_template.html':
#                 template_name = filename.rsplit('.', 1)[0]  # Remove the file extension
#                 with open(os.path.join(TEMPLATE_DIR, filename), 'r') as file:
#                     templates[template_name] = file.read()
#     return templates


# @app.route('/get_templates')
# def home():
#     # Get available templates to populate the dropdown
#     templates = get_available_templates()
#     return jsonify({"templates": templates})

# @app.route('/get_template/<template_name>')
# #@login_required
# def get_template(template_name):
#     # Dynamically fetch the template content from disk
#     templates = get_available_templates()
#     template = templates.get(template_name, "")
#     return jsonify({"template": template})


@app.route('/email_designs', defaults={'filename': None}, methods=['GET', 'POST'])
@app.route('/email_designs/<filename>', methods=['GET', 'POST'])
#@login_required
def email_designs(filename):
    archive_type = "email_designs"
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

# Web Page / Template Render / HTML   ########################################################################################
 
# Email editor
@app.route('/email_edit', methods=['GET'])
#@login_required
def email_edit():
    return send_file(f'{app_workdir}/templates/email_editor.html')#, templates=templates)    


@app.route('/email.css', methods=['GET'])
#@login_required
def email_css():
    return send_file(f'{app_workdir}/templates/email.css')#, templates=templates)  


@app.route('/email.js', methods=['GET'])
#@login_required
def email_js():
    return send_file(f'{app_workdir}/templates/email.js')#, templates=templates)  

# Helper function to save files in the user's directory
def save_design_files(user_id, design_id, html_content, json_content):
    USERS_BASE_DIR = f'{app_workdir}/app-files/users/{current_user.id}/email_designs'  # Store your HTML templates in this directory
    design_dir = os.path.join(USERS_BASE_DIR, f"design_{design_id}")
    os.makedirs(design_dir, exist_ok=True)

    html_path = os.path.join(design_dir, "design.html")
    json_path = os.path.join(design_dir, "design.json")

    with open(html_path, "w") as html_file:
        html_file.write(html_content)

    with open(json_path, "w") as json_file:
        json.dump(json_content, json_file)

    return design_dir

# Route to create and save a new design
@app.route('/save-design', methods=['POST'])
#@login_required
def save_template():
    try:
        # Extract data from the request
        data = request.json
        html_content = data.get("html")
        json_content = data.get("design")  # JSON content from Unlayer

        if not all([html_content, json_content]):
            return jsonify({"error": "Missing required fields"}), 400

        # Generate a unique design_id
        design_id = str(uuid.uuid4())  # Generate a unique identifier

        # Save the design to the database
        new_design = EmailDesign(
            design_id=design_id,
            html_content=html_content,
            json_content=json_content,
            user_id=current_user.id
        )
        db.session.add(new_design)
        db.session.commit()

        # Save the design files to the user's directory
        design_dir = save_design_files(
            user_id=current_user.id,
            design_id=design_id,
            html_content=html_content,
            json_content=json_content
        )

        return jsonify({
            "message": "Template saved successfully!",
            "design_id": design_id,
            "path": design_dir
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



# Helper function to create a directory for a new user
def create_user_directory(user_id):
    user_dir = os.path.join(USERS_BASE_DIR, f"{user_id}")
    os.makedirs(user_dir, exist_ok=True)
    return user_dir



@app.route('/email_design_preview')
#@login_required
def email_design_preview():
    try:
        with open(f'{app_workdir}/app-files/uploads/latest.html', 'r') as f:
            saved_template = f.read()
        return saved_template  # Return the saved template directly as the response
    except FileNotFoundError:
        return "Template not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/latest_template')
#@login_required
def get_saved_template():
    try:
        with open(f'{app_workdir}/app-files/uploads/latest.html', 'r') as f:
            saved_template = f.read()
        return jsonify({"template": saved_template})  # Return the saved template directly as the response
    except FileNotFoundError:
        return "Template not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    
@app.route('/latest_template_html')
#@login_required
def get_latest_template():
    try:
        with open(f'{app_workdir}/app-files/uploads/latest.html', 'r') as f:
            saved_template = f.read()
        return send_from_directory(f'{app_workdir}/app-files/uploads/', 'latest.html')
    except FileNotFoundError:
        return "Template not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload an image
@app.route('/upload-img', methods=['POST'])
#@login_required
def upload_img():
# Base directory for user images
    IMAGES_BASE_DIR = f'{app_workdir}/app-files/users/{current_user.id}/uploads/imgs'
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Validate the file type
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        # user_dir = os.path.join(IMAGES_BASE_DIR, str(current_user.id))
        os.makedirs(IMAGES_BASE_DIR, exist_ok=True)
        file_path = os.path.join(IMAGES_BASE_DIR, filename)
        file.save(file_path)

        # Save the file metadata in the database
        new_image = Image(
            image_name=filename,
            image_path=file_path,
            user_id=current_user.id
        )
        db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully!", "path": file_path, "url": f"http://{fqdn}:{port}/users/{current_user.id}/imgs/{filename}"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
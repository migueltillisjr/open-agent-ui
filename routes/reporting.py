from . import *




# Reporting Routes ############################################################################################################################
@app.route('/notify_report', methods=['GET'])
# #@login_required
def notify_report():
    return send_file(f'{app_workdir}/app-files/users/{current_user.id}/templates/notify.html')


@app.route('/reports', defaults={'filename': None}, methods=['GET', 'POST'])
@app.route('/reports/<filename>', methods=['GET', 'POST'])
# #@login_required
def reports(filename):
    archive_type = "reports"
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
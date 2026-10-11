
from flask import Flask, request, redirect, render_template_string, send_file
import dropbox
from io import BytesIO
import os

app = Flask(__name__)

# Enter your Dropbox Access Token here
ACCESS_TOKEN = "PASTE_YOUR_DROPBOX_ACCESS_TOKEN_HERE"

# Connect to Dropbox
dbx = dropbox.Dropbox(ACCESS_TOKEN)

try:
    account = dbx.users_get_current_account()
    print("Connected to:", account.name.display_name)
    print("Dropbox connected successfully!")

except Exception as e:
    print("Connection failed:", e)
    raise SystemExit(1)


# Home Page - Display Files
@app.route("/")
def home():

    result = dbx.files_list_folder("")

    files = []

    for file in result.entries:
        if isinstance(file, dropbox.files.FileMetadata):
            files.append(file.name)

    while result.has_more:
        result = dbx.files_list_folder_continue(result.cursor)

        for file in result.entries:
            if isinstance(file, dropbox.files.FileMetadata):
                files.append(file.name)

    with open("index.html", encoding="utf-8") as f:
        html = f.read()

    return render_template_string(html, files=files)


# Upload File to Dropbox
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    if not file or not file.filename:
        return "Please select a file!", 400

    filename = os.path.basename(file.filename.replace("\\", "/"))

    if not filename.lower().endswith((".pdf", ".txt")):
        return "Only PDF and TXT files allowed!", 400

    try:
        dbx.files_upload(
            file.read(),
            "/" + filename,
            mode=dropbox.files.WriteMode.overwrite
        )

        print(filename, "Uploaded Successfully!")

        return redirect("/")

    except Exception as e:
        return "Upload failed: " + str(e), 500


# Download File from Dropbox
@app.route("/download/<path:filename>")
def download(filename):

    filename = os.path.basename(filename)

    if not filename.lower().endswith((".pdf", ".txt")):
        return "Invalid file type!", 400

    try:
        metadata, response = dbx.files_download("/" + filename)

        return send_file(
            BytesIO(response.content),
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return "Download failed: " + str(e), 500


# Run Flask Application
if __name__ == "__main__":
    app.run(debug=False)

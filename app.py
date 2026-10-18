
from flask import Flask, request, redirect, render_template_string, send_file
import dropbox
from io import BytesIO
import os
from pathlib import Path

app = Flask(__name__)

ACCESS_TOKEN = ""


def get_dropbox_client():
    if not ACCESS_TOKEN:
        app.logger.warning("ACCESS_TOKEN is empty. Dropbox features are disabled.")
        return None

    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    try:
        account = dbx.users_get_current_account()
        print("Connected to:", account.name.display_name)
        return dbx
    except Exception as exc:
        app.logger.warning("Dropbox authentication failed: %s", exc)
        return None


dbx = get_dropbox_client()


# Home Page - Display Files
@app.route("/")
def home():
    files = []

    if dbx is not None:
        try:
            result = dbx.files_list_folder("")

            for file in result.entries:
                if isinstance(file, dropbox.files.FileMetadata):
                    files.append(file.name)

            while result.has_more:
                result = dbx.files_list_folder_continue(result.cursor)

                for file in result.entries:
                    if isinstance(file, dropbox.files.FileMetadata):
                        files.append(file.name)
        except Exception as exc:
            app.logger.error("Dropbox file listing failed: %s", exc)
            return f"Unable to list Dropbox files: {exc}", 500

    html_path = Path(__file__).with_name("index.html")
    with html_path.open("r", encoding="utf-8") as f:
        html = f.read()

    return render_template_string(html, files=files)


# Upload File to Dropbox
@app.route("/upload", methods=["POST"])
def upload():
    if dbx is None:
        return "Dropbox is not configured. Set DROPBOX_ACCESS_TOKEN before uploading.", 503

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
            mode=dropbox.files.WriteMode.overwrite,
        )

        print(filename, "Uploaded Successfully!")

        return redirect("/")
    except Exception as e:
        return "Upload failed: " + str(e), 500


# Download File from Dropbox
@app.route("/download/<path:filename>")
def download(filename):
    if dbx is None:
        return "Dropbox is not configured. Set DROPBOX_ACCESS_TOKEN before downloading.", 503

    filename = os.path.basename(filename)

    if not filename.lower().endswith((".pdf", ".txt")):
        return "Invalid file type!", 400

    try:
        metadata, response = dbx.files_download("/" + filename)

        return send_file(
            BytesIO(response.content),
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        return "Download failed: " + str(e), 500


# Run Flask Application
if __name__ == "__main__":
    app.run(debug=False)

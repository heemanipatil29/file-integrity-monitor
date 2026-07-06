
from flask import Flask, request
import hashlib
import os
app= Flask(__name__)
FOLDER_UPLOAD = "upload"
if not os.path.exists(FOLDER_UPLOAD):
    os.mkdir(FOLDER_UPLOAD)
stored_hash = ""
uploaded_file_path = ""
file_to_monitor = ""
def generate_hash(uploaded_file_path):

    sha256 = hashlib.sha256()

    with open(uploaded_file_path, "rb") as file:

        while True:

            data = file.read(4096)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

@app.route("/")
def home ():

    return """
    <html>
    <head>
    <body style="background-color:#13072a; color:#00BFFF; font-family:Arial; text-align:center;">
    <h1 style="font-size:50px; color:#ffffff;">File Integrity Monitor</h1>
    <h2> Select File</h2>
    <form action="/scan" method="POST" enctype="multipart/form-data">
    <input type="file" name="file" style="width:300px; height:40px;"><br><br>
    <button style="width:200px; height:60px; background-color:#13072a; color:#00BFFF; font-size:22px; font-weight:bold; border-radius:10px; box-shadow:0 0 15px #00FF88;">SCAN FILE</button></form>
    
   
    </body></head></html
     """
@app.route("/scan", methods=["POST"])   
def scan():
    global stored_hash
    global uploaded_file_path
    file = request.files["file"]
    uploaded_file_path = os.path.join(FOLDER_UPLOAD, file.filename)

    uploaded_file_path = os.path.join(FOLDER_UPLOAD, file.filename)
    file.save(uploaded_file_path)
    stored_hash = generate_hash(uploaded_file_path)
    print(uploaded_file_path)
    global file_to_monitor
    file_to_monitor = uploaded_file_path
    print("Saved File Path:", uploaded_file_path)
    print("Stored Hash:", stored_hash)
    
    return f"""
    <html>
    <body style="background-color:#13072a; color:#00BFFF; font-family:Arial; text-align:center;">
    <h1 style="font-size:50px; color:#ffffff;">File Integrity Monitor</h1>
    <h2>File name:{file.filename}</h2>
    <h3>sha256 hash Generated:</h3>
    <p style="color:#00FF88; word-break:break-all;">{stored_hash}</p>
    <h2 style="color:#00FF88;">Hash Stored Successfully ✅</h2><br><br>
    <form action="/monitor" method="POST">
    <button type="submit";style="width:220px;height:60px;background:#13072a;color:#00FF88;font-size:22px;font-weight:bold;border-radius:10px;">
    START MONITORING
    </button>
    </form>
    </body></html>
    """
@app.route("/monitor", methods=["POST"])
def monitor():
    global stored_hash
    global uploaded_file_path
    print("MONITORING:", uploaded_file_path)
    current_hash = generate_hash(uploaded_file_path)
    if current_hash == stored_hash:
        result = "File Safe ✅"
        color = "#00FF88"
    else:
        result = "File Modified ⚠️"
        color = "red"

    print("Monitoring File:", uploaded_file_path)
    print("Stored Hash:", stored_hash)
    print("Current Hash:", current_hash)
    return f"""
    <html>
    <body style="background-color:#13072a; color:#00BFFF; font-family:Arial; text-align:center;">
    <h1 style="font-size:50px; color:#ffffff;">File Integrity Monitor</h1>
    <h2 style="color:{color};">{result}</h2>
    <h3> Stored Hash:</h3>
    <p style="color:#00FF88;word-break:break-all;">{stored_hash}</p>
    <h3> Current Hash:</h3>
    <p style="color:#00FF88;word-break:break-all;">{current_hash}</p>
    </body></html>
    """
app.run(debug=True)

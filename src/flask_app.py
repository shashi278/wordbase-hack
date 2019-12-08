from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

from main import solve

UPLOAD_FOLDER = 'tmp/wordbase-images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__, template_folder="statics")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def nothing():
    return "Nothing here"

@app.route("/wordbase-hack")
def upload():
    return render_template("file_upload_form.html", title="color-filter-upload", err_msg="")

@app.route('/solve', methods=['POST'])
def solver():
    file = request.files['file']
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if file and allowed_file(file.filename):
        color = request.form["color"]
        filename = secure_filename(file.filename)
        try:
            intersection= request.form["intersection"]
        except KeyError: intersection= None
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(img_path)

        results= None
        if intersection is None:
            print("intersection is none")
            results = solve(img_path, color, only_intersection=False)
            print(len(results))
        else:
            print("intersection not none")
            results = solve(img_path, color)
            print(len(results))

        os.system("rm -rf {}".format(UPLOAD_FOLDER))
        if results:
            return str(len(results)) #render_template("result.html", len= len(results), results=results, filter_info="c= {}, int= {}".format(color,intersection))
        return "Empty result :("
    return render_template("file_upload_form.html", err_msg="Please select an image", title="Error")


if __name__ == "__main__":
    app.run(debug=True, port=8002)
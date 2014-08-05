from flask import Flask, url_for, redirect, render_template
import os
import datetime


app = Flask(__name__)

photo_dir = "/home2/slowerin/www/drone-daydream/static/photos"
like_dir = "/home2/slowerin/www/drone-daydream/static/likes"


perpage = 20

@app.route('/admin/', defaults={"admin": True})
@app.route('/admin/page/<int:pagenum>', defaults={"admin": True})
@app.route('/')
@app.route('/page/<int:pagenum>')
def index(pagenum=1, admin=False, scroll=False):
    photos = get_photo_list()[(pagenum-1)*perpage : (pagenum)*perpage]   
    for p in photos:
        p["date"] = datetime.datetime.fromtimestamp(int(p["date"])).strftime("%B %d, %Y")
        p["likes"] = get_likes(p["name"])
    
    request = { "photos": photos, "pagenum":pagenum, "admin": admin, "scroll":scroll}
    return render_template("index.html", request=request)

@app.route('/admin/scroll/<int:pagenum>', defaults={"admin": True})
@app.route('/scroll/<int:pagenum>')
def scroll(pagenum, admin=False):
    return index(pagenum, admin, True)

@app.route('/like/<file>')
def like(file):
    count = 0
    if ".." not in file and "/" not in file:
        with open(os.path.join(like_dir, file + ".dat"), "a+") as f:
            pass
        with open(os.path.join(like_dir, file + ".dat"), "r+") as f:
            f.seek(0)
            try:
                count = int(f.readline())
            except ValueError:
                count = 0

            f.seek(0)
            f.write(str(count + 1))
            count += 1

    return str(count)

@app.route('/admin/page/<int:pagenum>/hide/<file>')
def hide(pagenum,file):
    if ".." not in file and "/" not in file:
        os.rename(os.path.join(photo_dir, file), os.path.join(photo_dir, "hidden", file))
    return redirect(url_for("index", pagenum=pagenum, admin=True))

def get_photo_list():
    os.chdir(photo_dir)
    files = filter(os.path.isfile, os.listdir(photo_dir))
    photos = [{"name": f, "date": os.path.getmtime(os.path.join(photo_dir, f))} for f in files]
    photos.sort(key=lambda x: x["date"], reverse=True)
    return photos

def get_likes(file):
    count = 0
    try:
        with open(os.path.join(like_dir, file + ".dat"), "r") as f:
            count = int(f.readline())
    except Exception:
        count = 0

    return count

app.debug = True
if __name__ == "__main__":
    app.run()

import os
from bottle import route, request, static_file, run

@route('/')
def root():
    return static_file('test.html', root='.')

@route('/upload', method='POST')
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.bmp', '.png', '.jpg', '.jpeg' ):
        return "Файл з таким розширенням не підтримується. Підтримуються: bmp, jpg, png, jpeg."

    save_path = "/tmp/meter values/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "Файл збережено в {0}".format(save_path)

if __name__ == '__main__':
    run(host='localhost', port=8080)
from waitress import serve
from socres.wsgi import application
import os
from socres.settings import STATIC_ROOT


if __name__ == '__main__':
    this_files_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(this_files_dir)
    serve(application, host='0.0.0.0', port=8000)
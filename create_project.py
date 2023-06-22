import os

def create_project_dir_structure():
    base_path = os.getcwd()
    dirs = [
        'static/css',
        'static/js',
        'templates'
    ]

    for dir in dirs:
        os.makedirs(os.path.join(base_path, dir), exist_ok=True)

    files = [
        'app.py',
        'requirements.txt',
        'static/css/style.css',
        'static/js/script.js',
        'templates/index.html',
        'templates/report.html'
    ]

    for file in files:
        open(os.path.join(base_path, file), 'a').close()

# Use it like this:
create_project_dir_structure()

import os
from shutil import rmtree
from repositories.repository_manager import RepositoryManager
from repositories.repository import Repository
from users.user import User
from datetime import date
from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)
repo_manager = RepositoryManager()

if os.path.exists('/tmp/repos'):
    rmtree('/tmp/repos')
os.makedirs('/tmp/repos')
with open('/tmp/repos/repolist', 'w') as repo_list:
    repo_list.write('repo1\n')
    repo_list.write('repo2\n')
repo1 = Repository('repo1', '/tmp/repos/repo1')
alice = User('Alice', 'Smith', date(1980, 10, 10), 'alice@mail.org', '****')
bob = User('Bob', 'Marker', date(1970, 11, 11), 'bob@mail.org', '****')
alice_id = repo1._user_manager.add_user(alice)
bob_id = repo1._user_manager.add_user(bob)
repo1.import_documents('/tmp/samples/importable')


@app.route('/repos/')
def index():
    repos = repo_manager.load_repos('/tmp/repos')
    return render_template('repos.html', repos=repos)


@app.route('/repos/<repo_name>')
def show_repo(repo_name):
    repo = repo_manager._repos[repo_name]
    docs = repo._document_manager.list_documents()
    return render_template('repo.html', repo_name=repo_name, docs=docs)


@app.route('/repos/<repo_name>/<int:doc_id>')
def show_doc(repo_name, doc_id):
    repo = repo_manager._repos[repo_name]
    info = repo._document_manager.info_file_path(doc_id)
    with open(info) as info_file:
        title = info_file.readline().rstrip('\n')
        description = info_file.readline().rstrip('\n')
        author = int(info_file.readline().rstrip('\n'))
        files = info_file.readline().rstrip('\n').split(',')
        doc_format = info_file.readline().rstrip('\n')
        state = info_file.readline().rstrip('\n')
        is_public = True if info_file.readline().rstrip('\n') == 'True' else False
    return render_template('doc.html', title=title, description=description,
                           author=author, files=files, doc_format=doc_format,
                           state=state, is_public=is_public, repo_name=repo_name)


if __name__ == '__main__':
    app.run(port=8081, host='0.0.0.0')

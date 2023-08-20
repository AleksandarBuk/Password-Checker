import requests
import hashlib
from flask import Flask, render_template, request, flash
import click

app = Flask(__name__)
app.secret_key = 'secret_key'


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fatching {res.status_code}, check the API and try agian')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


@click.command()
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Password to check")
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        count = pwned_api_check(password)
        if count:
            flash(
                f'This password was found {count} times. You should probably change your password.', 'warning')
        else:
            flash(f'{password} was not found. Carry on!', 'success')
    return render_template('index.html')

#add tinker user interface/Pyside6

#add suggestions on how to create a safe password


if __name__ == '__main__':
    app.run()

import requests
import hashlib
from flask import Flask, render_template, request, flash
import click
import secrets
import string

def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for i in range(length))
    return secret_key


app = Flask(__name__)
app.secret_key = 'f;jQb2d4Zu>mEWF$)h=<S}"t'

PWNED_PASSWORDS_API_URL = 'https://api.pwnedpasswords.com/range/'


def request_api_data(query_char):
    url = PWNED_PASSWORDS_API_URL + query_char
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        return res
    except requests.exceptions.RequestException as e:
        flash(f'Error fetching data from the API: {e}', 'danger')
        return None


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        first5_char, tail = sha1password[:5], sha1password[5:]
        response = request_api_data(first5_char)

        if response is not None:
            count = get_password_leaks_count(response, tail)
            if count:
                flash(
                    f'This password was found {count} times. You should probably change your password.', 'warning')
            else:
                flash(f'{password} was not found. Carry on!', 'success')

    return render_template('index.html')


# Custom error handling for 404 (Page Not Found) errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message='Page not found'), 404


# Custom error handling for 500 (Internal Server Error) errors
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='Internal server error'), 500


if __name__ == '__main__':
    app.run()


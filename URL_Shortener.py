from flask import Flask, request, redirect
import hashlib

app = Flask(__name__)

url_mapping = {}

def generate_short_url(long_url):
    hash_object = hashlib.md5(long_url.encode())
    # Using the first 8 characters of the MD5 hash as the short URL
    return hash_object.hexdigest()[:8]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url(long_url)
        url_mapping[short_url] = long_url
        return f'Short URL: {request.host_url}{short_url}'
    return '''
        <form method="post">
            Long URL: <input type="text" name="long_url">
            <input type="submit" value="Shorten">
        </form>
    '''

@app.route('/<short_url>')
def redirect_to_original(short_url):
    if short_url in url_mapping:
        return redirect(url_mapping[short_url])
    return 'Short URL not found'

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form():
    print(request.form)
    if "alice_string" in request.form and "bob_string" in request.form:
        print("form entry")
        alice_bits = request.form['alice_string']
        bob_bits = request.form['bob_string']
        return render_template('form return.html',alice_bits=alice_bits,bob_bits=bob_bits,corrected_string="corrected_string",no_parity="no_parity",no_errors="no_errors",shannon_limit="shannon_limit",no_itterations="no_itterations")
    else:
        return ("<h1>ERROR</h1>")
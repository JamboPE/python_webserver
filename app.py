from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form():
    alice_bits = request.form['alice_string']
    bob_bits = request.form['bob_string']
    for character in alice_bits:
        if character != '0' and character != '1':
            return render_template('form error.html', error="You must enter a binary string!")
    for character in bob_bits:
        if character != '0' and character != '1':
            return render_template('form error.html', error="You must enter a binary string!")
    if len(alice_bits) != len(bob_bits):
        return render_template('form error.html', error="The two keys must be the same length!")
    if alice_bits == alice_bits:
        return render_template('form return.html',alice_bits=alice_bits,bob_bits="  "+str(bob_bits),corrected_string="corrected_string",no_parity="no_parity",no_errors="no_errors",shannon_limit="shannon_limit",no_itterations="no_itterations")
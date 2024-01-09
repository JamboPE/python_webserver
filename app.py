from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    alice_bits = request.form['alice_string']
    bob_bits = request.form['bob_string']
    print (alice_bits)
    print (bob_bits)
    return render_template('form return.html',alice_bits=alice_bits,bob_bits=bob_bits,corrected_string="corrected_string",no_parity="no_parity",no_errors="no_errors",shannon_limit="shannon_limit",no_itterations="no_itterations")
#if __name__ == '__main__':
#    app.run(debug=True)
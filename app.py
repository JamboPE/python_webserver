from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', background_color="", text_color="")

@app.route('/', methods=['POST'])
def form():
    print(request.form)
    if "alice_string" in request.form and "bob_string" in request.form:
        print("form entry")
        alice_bits = request.form['alice_string']
        bob_bits = request.form['bob_string']
        try:
            dark_mode
        except:
            dark_mode = False
        if dark_mode == True:
            return render_template('form return.html',alice_bits=alice_bits,bob_bits=bob_bits,corrected_string="corrected_string",no_parity="no_parity",no_errors="no_errors",shannon_limit="shannon_limit",no_itterations="no_itterations", background_color="rgb(80, 80, 80)", text_color="white")
        else:
            return render_template('form return.html',alice_bits=alice_bits,bob_bits=bob_bits,corrected_string="corrected_string",no_parity="no_parity",no_errors="no_errors",shannon_limit="shannon_limit",no_itterations="no_itterations", background_color="", text_color="")
    elif "tesco" in request.form:
        dark_mode = True
        return render_template('index.html', background_color="rgb(80, 80, 80)", text_color="white") # Dark Mode
    else:
        dark_mode = False
        return render_template('index.html', background_color="", text_color="") # Light Mode
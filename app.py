from flask import Flask, render_template, request
import math
import cascade

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
    processed_data=cascade.process_input_data(alice_bits,bob_bits)
    no_bits = processed_data[0]
    no_errors = processed_data[1]
    error_array = processed_data[2]
    error_rate = processed_data[3]
    omega = processed_data[4]
    if no_errors < 2:
        parities=cascade.check_parity(alice_bits,bob_bits)
        alice_parity = parities[0]
        bob_parity = parities[1]
        split_arrays = parities[2]
        split_arrays2 = parities[3]
        table_data = cascade.show_table(cascade.string_to_array(alice_bits),alice_parity,cascade.string_to_array(bob_bits),bob_parity,error_array,no_errors,split_arrays,split_arrays2)
        no_parity = (len(split_arrays)*2)
    else:
        table_data = [cascade.string_to_array(alice_bits),cascade.string_to_array(bob_bits),error_array]
        no_parity = math.ceil(cascade.h_func(error_rate)*no_bits)
    ratio_parity_shannon = (no_parity/no_bits)/cascade.h_func(error_rate)
    return render_template('form return.html',alice_bits=str(alice_bits),bob_bits=str(bob_bits),corrected_string=str(alice_bits),no_parity=no_parity,naive_parity="<naive_parity>",optimal_parity="<optimal_parity>",no_errors=str(no_errors),shannon_limit=cascade.h_func(error_rate),ratio_shannon=ratio_parity_shannon,no_itterations="no_iterations",tbl=table_data,omega=omega,string_length=len(str(alice_bits)),no_bits=no_bits)
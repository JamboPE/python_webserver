#app.py - hosts the error correction web server using Flask
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
    ### functionise this bit
    no_bits = processed_data[0]
    no_errors = processed_data[1]
    error_array = processed_data[2]
    error_rate = processed_data[3]
    omega = processed_data[4]
    if no_errors < 2:
        # splits both arrays in half and gives the parity of each half for both strings (returns as a list)
        parities=cascade.check_parity(alice_bits,bob_bits)
        alice_parity = parities[0]
        bob_parity = parities[1]
        split_arrays = parities[2]
        split_arrays2 = parities[3]
        # run the cascade algorithm and output results to a html table
        table_data = cascade.show_table(cascade.string_to_array(alice_bits),alice_parity,cascade.string_to_array(bob_bits),bob_parity,error_array,no_errors,split_arrays,split_arrays2)
        no_parity = (len(split_arrays)*2) # Calculate the number of parity bits exposed
    else:
        # run the cascade algorithm and output results to a html table
        table_data = [cascade.string_to_array(alice_bits),cascade.string_to_array(bob_bits),error_array]
        no_parity = math.ceil(cascade.h_func(error_rate)*no_bits)
    ratio_parity_shannon = (no_parity/no_bits)/cascade.h_func(error_rate) # calculate the ratio of parity bits to the shannon limit
    #return the results to the user in a html table using the template 'form return.html'
    return render_template('form return.html',alice_bits=str(alice_bits),bob_bits=str(bob_bits),corrected_string=str(alice_bits),no_parity=no_parity,naive_parity="<naive_parity>",optimal_parity="<optimal_parity>",no_errors=str(no_errors),shannon_limit=cascade.h_func(error_rate),ratio_shannon=ratio_parity_shannon,no_itterations="no_iterations",tbl=table_data,omega=omega,string_length=len(str(alice_bits)),no_bits=no_bits)

# API
def api_error(api_function, api_call, syntax, error):
    host = "http://" + request.host + "/api/" + api_function + "/"
    return """Invalid API call!
>>>    '""" + host + api_call + """'
Error: """ + error + """
Please use the syntax:
'""" +host+syntax+"'"

@app.route('/api')
def api_index():
    return """Welcome to the API!
You can make a call using the syntax 'http://""" + request.host + """/api/cascade/<Alice's String>/<Bob's String>'"""
@app.route('/api/')
def api_index2():
    return """Welcome to the API!
You can make a call using the syntax 'http://""" + request.host + """/api/cascade/<Alice's String>/<Bob's String>'"""

## API functions
def api_cascade(api_call):
    api_function = "cascade"
    syntax = "<Alice's String>/<Bob's String>"
    api_call_array = api_call.split('/')
    if len(api_call_array) <= 1:
        return api_error(api_function, api_call, syntax, "No '/' found in the API path.")
    elif len(api_call_array) > 3:
        return api_error(api_function, api_call, syntax, "More than two '/' found in the API path.")
    elif len(api_call_array) != 2:
        if api_call_array[2] != "":
            return api_error(api_function, api_call, syntax, "More than two strings found in the API path.")
    if api_call_array[1] == "":
        return api_error(api_function, api_call, syntax, "Only one string found in the API path.")
    alice_bits = api_call_array[0]
    bob_bits = api_call_array[1]
    for character in alice_bits:
        if character != '0' and character != '1':
            return api_error(api_function, api_call, syntax, "Alice's String contains non binary characters.")
    for character in bob_bits:
        if character != '0' and character != '1':
            return api_error(api_function, api_call, syntax, "Bob's String contains non binary characters.")
    if len(alice_bits) != len(bob_bits):
        return api_error(api_function, api_call, syntax, "The strings must be the same length.")
    processed_data=cascade.process_input_data(alice_bits,bob_bits)
    ### functionise this bit
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
    return """{"status":"OK","payload":"'Corrected_Key':'"""+str(alice_bits)+"""','Key_Length':'"""+str(len(str(alice_bits)))+"""','Wrong_Parity':'"""+str(no_parity)+"""','Number_Errors':'"""+str(no_errors)+"""','Shannon_Limit':'"""+str(cascade.h_func(error_rate))+"""','Shannon_Ratio':'"""+str(ratio_parity_shannon)+"""','Cascade_Itterations':'"""+"no_iterations"+"""'"}"""

@app.route('/api/<path:api_function>')
def api(api_function):
    api_function_array = api_function.split('/')
    api_call = ""
    if len(api_function_array) > 1:
        for entry in api_function_array[1:]:
            api_call += entry + "/"
        api_call = api_call[:-1]
    if api_function_array[0] == "cascade":
        return api_cascade(api_call)
    else:
        return """Invalid API call!
>>>    'http://"""+ request.host + "/api/" + api_function + """'
Did you mean 'http://""" + request.host + "/api/cascade/<Alice's String>/<Bob's String>/'?"
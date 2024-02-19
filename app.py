from flask import Flask, render_template, request

import subprocess
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    return output

def remove_symbols(string,array,replacement):
    new_string = ""
    #for character in string:
    #    if character in array:
    #        pass
    #    else:
    #        new_string = new_string + character
    for i in range(0,len(string)):
        two_symbols = False
        try:
            if str(string[i])+str(string[i+1]) in array:
                two_symbols = True
                new_string = new_string + replacement
            elif string[i] in array:
                new_string = new_string + replacement
            elif two_symbols == False:
                new_string = new_string + string[i]
            else:
                pass
        except:
            if string[i] in array:
                new_string = new_string + replacement
            elif two_symbols == False:
                new_string = new_string + string[i]
            else:
                pass
    return new_string

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
        script_output = run_command(["/usr/bin/python", "/home/jambo/Documents/Coding/Uni/qkd-webserver/cascade.py", bob_bits, alice_bits])
        script_split = script_output.split('\n')
        script_output = script_split[0]
        script_output = remove_symbols(script_output,["[[","]]"],"")
        script_output_lines = script_output.split('], [')
        script_output_lines_pruned = []
        for line in script_output_lines:
            script_output_lines_pruned.append(remove_symbols(line,["[","]",'"',"'"],""))
        script_output_lines_app = []
        for line in script_output_lines_pruned:
            script_output_lines_app.append(remove_symbols(line,["|"],"'"))
        script_output_lines_table = []
        for line in script_output_lines_app:
            script_output_lines_table.append(line.split(','))
        return render_template('form return.html',alice_bits=alice_bits,bob_bits="  "+str(bob_bits),corrected_string=str(alice_bits),no_parity=script_split[2],no_errors=script_split[3],shannon_limit=script_split[4],no_itterations=script_split[5],tbl=script_output_lines_table)#tbl=zip(*script_output_lines))

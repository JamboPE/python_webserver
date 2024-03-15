import math
import random
import sys

def string_to_array(string): # Used for user display purposes to convert each character in a string to entries in an array
    array=[]
    for i in string: # iterate through each character in the string
        array.append(i) # append each character to the array
    return array

def process_input_data(alice_bits, bob_bits):
    #bob_bits = string_to_array(sys.argv[1])
    #alice_bits = string_to_array(sys.argv[2])
    no_bits =  len(bob_bits)
    no_errors = 0
    error_array = []
    if bob_bits == alice_bits:
        for line in bob_bits:
            error_array.append(" ")
        error_rate = 0
    else:
        for i in range(0,len(bob_bits)):
            if bob_bits[i] != alice_bits[i]:
                no_errors += 1
                error_array.append("X")
            else:
                error_array.append(" ")
        error_rate = no_errors/no_bits
    if error_rate != 0:
        omega = 0.73/error_rate
    else:
        omega = "N/A, there are no errors in the strings"
    return [no_bits, no_errors, error_array, error_rate, omega]

def array_to_string(array): # Used for user display purposes to convert each entry in an array to characters in a string
    string=""
    for i in array: # iterate through each entry in the array
        string = string + i # append each entry to the string
    return string

def generate_random_bits(length): # Used to generate a random array of 1s and 0s of a given length
    binary_string = ''.join(random.choice('01') for _ in range(length)) # generate a random string of 1s and 0s of a given length
    return string_to_array(binary_string) # Convert the string to an array and return it

def generate_random_bases(length): # Used to generate a random array of Ds and Rs of a given length
    bases_string = ''.join(random.choice('DR') for _ in range(length)) # generate a random string of Ds and Rs of a given length
    return string_to_array(bases_string) # Convert the string to an array and return it

def test_percentage(prob): # Essentially a coin flip with a given probability, has the given probability of returning true 
    # generate a random float between 0 and 1
    if random.random() < (prob/100): # if the float is less than the probability as a decimal, return true
        return True
    else: # otherwise, return false
        return False
    
def parity_sum(array): # Used to calculate the sum of all entries in an array
    total=0
    for i in array: # iterate through each entry in the array
        i = int(i)
        total=total+i # add each entry to the total
        if total == 2: # binary addition, so if the total is 2, set it to 0
            total=0
    return total

def split_array(array1, array2): # Used to split two arrays into two halves
    low_array1=[]
    up_array1=[]
    low_array2=[]
    up_array2=[]
    LB=0 # set the lower bound to 0
    UB=len(array1)-1 # set the upper bound to the length of the array minus 1
    mid=(LB+UB)//2 # find the middle index
    for i in range(0,len(array1)):
        if i <= mid:
            low_array1.append(array1[i])
            low_array2.append(array2[i])
        else:
            up_array1.append(array1[i])
            up_array2.append(array2[i])
    if len(up_array1) != len(up_array2) or len(low_array1) != len(low_array2) or parity_sum(low_array1) == parity_sum(low_array2) and parity_sum(up_array1) == parity_sum(up_array2):
        return "split_array() Error: The lengths of the arrays are not equal or the parity sums of the arrays are equal"
    elif parity_sum(low_array1) != parity_sum(low_array2) and parity_sum(up_array1) == parity_sum(up_array2):
        return [low_array1, low_array2, "low",len(up_array1)]
    elif parity_sum(low_array1) == parity_sum(low_array2) and parity_sum(up_array1) != parity_sum(up_array2):
        return [up_array1, up_array2, "up",len(low_array1)]
    else:
        return "Error"

def cascade(correct_array, incorrect_array):
    split_arrays=[]
    split_arrays2=[]
    bounds=[]
    alice_array = []
    bob_array = []
    no_bits = len(correct_array)
    size_of_other_array = []
    while len(correct_array) != 1:
        both_arrays = split_array(correct_array, incorrect_array)
        correct_array = both_arrays[0]
        incorrect_array = both_arrays[1]
        size_of_other_array.append(both_arrays[3])
        if both_arrays[2] == "low":
            bounds.append("low")
        elif both_arrays[2] == "up":
            bounds.append("up")
        else:
            return "Error"
        alice_array.append(correct_array)
        bob_array.append(incorrect_array)
    final_array = add_spaces(alice_array, bob_array, bounds,size_of_other_array)
    return [final_array[0],final_array[1]]

def add_spaces(alice_array, bob_array,bounds,size_of_other_array):
    total_front_spaces = 0
    total_back_spaces = 0
    for i in range(0,len(alice_array)):
        if bounds[i] == "low":
            total_back_spaces += size_of_other_array[i]
        elif bounds[i] == "up":
            total_front_spaces += size_of_other_array[i]
        for j in range (0,total_back_spaces):
                alice_array[i].append(" ")
                bob_array[i].append(" ")
        alice_temp = []
        bob_temp = []
        for j in range (0,total_front_spaces):
            alice_temp.append(" ")
            bob_temp.append(" ")
        for entry in alice_array[i]:
            alice_temp.append(entry)
        for entry in bob_array[i]:
            bob_temp.append(entry)
        alice_array[i] = alice_temp
        bob_array[i] = bob_temp
    for i in range(0,len(alice_array)):
        alice_array[i].insert(0,"Alice")
        bob_array[i].insert(0,"Bob")
        alice_array[i].append(" ")
        alice_array[i].append(" ")
        bob_array[i].append(" ")
        bob_array[i].append(" ")
    return [alice_array,bob_array]

def h_func(p):
    if p != 0:
        h = (-1 * p * math.log2(p)) - ((1-p) * math.log2(1-p)) # Shannon entropy
    else:
        h = 0
    return h

###################################################################################
def split_into_subblocks(string,omega):
    substring_size = omega
    no_subblock = math.ceil(string / substring_size)
    subblock = 0
    bit = 0
    subblocks=[]
    for i in range(0,len(string)):
        if subblock == no_subblock and bit == 0:
                subblocks.append(string[i:])
        elif bit == 0 and subblock != no_subblock:
            subblocks.append(string[i:i+substring_size])
        elif bit == substring_size-1:
            bit = -1
            subblock += 1        
        bit += 1
    return subblocks
###################################################################################

def check_parity(alice_bits,bob_bits):
    alice_parity, bob_parity = parity_sum(alice_bits), parity_sum(bob_bits) # Calculate the parity of Alice's and Bob's bits
    if alice_parity == bob_parity: # If the parity of Alice's and Bob's bits are the same, do not use the cascade method
        pass
        split_arrays_array = [[False],[False]]
    else:
        split_arrays_array=cascade(alice_bits,bob_bits) # Otherwise, use the cascade method to find the error
    return [alice_parity, bob_parity, split_arrays_array[0], split_arrays_array[1]]

def show_table(alice,a_parity,bob,b_parity,error_array,no_errors,split_arrays,split_arrays2):
    alice.insert(0,'Alice\'s Key')
    alice.append(' Parity Value')
    alice.append(a_parity)
    bob.insert(0,'Bob\'s Key')
    bob.append(' Parity Value')
    bob.append(b_parity)
    error_array.insert(0, 'Errors')
    error_array.append(' Total Errors ')
    error_array.append(no_errors)
    data = [alice,bob,error_array]
    for i in range(0,len(split_arrays)):
        if split_arrays[0] != False or split_arrays2[0] != False:
            data.append(split_arrays2[i])
            data.append(split_arrays[i])
    return data

# ^This is the Shannon limit for the cascade protocol - Most ideal case - ideal percentage of bits that would need to be given up as parity bits to correct the error
# Need to impliment a ratio (higher than 1) of the percentage of bits my cascade gives up commpared to the Shannon limit
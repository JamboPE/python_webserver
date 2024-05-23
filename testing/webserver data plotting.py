import requests
import matplotlib.pyplot as plt

url = 'http://localhost'
port = '2000'
api_call = '/api/cascade/'
url = url + ':' + port + api_call

def get_shannon_limit(alice,bob):
    x = requests.get(url+alice+'/'+bob)
    useful_data0 = x.text.split(',')[3]
    useful_data0 = useful_data0.split(':')
    useful_data = x.text.split(',')[5]
    useful_data = useful_data.split(':')
    useful_data2 = x.text.split(',')[6]
    useful_data2 = useful_data2.split(':')

    if useful_data[0].strip("'") == "Shannon_Limit" and useful_data2[0].strip("'") == "Shannon_Ratio" and useful_data0[0].strip("'") == "Wrong_Parity":
        return [useful_data[1].strip("'") , useful_data2[1].strip("'").strip("}").strip('"')[0:-1], useful_data0[1].strip("'")]
    else: 
        print("Error in getting Shannon Limit or Shannon Ratio")
        exit(1)

Shannon_array = []
Ratio_array = []
Parity_array = []
x = []
alice_string = "10"
bob_string = "00"

for i in range(1,255):
    data = get_shannon_limit(alice_string,bob_string)
    Shannon_array.append(float(data[0]))
    Ratio_array.append(float(data[1]))
    Parity_array.append(int(data[2]))
    x.append(i+1)
    alice_string += "0"
    bob_string += "0"

plt.plot(x,Shannon_array)
#plt.plot(x,Ratio_array)
#plt.plot(x,Parity_array)
plt.title('Graph of ratio of bits exposed to string length vs string length')
plt.xlabel('String length')
plt.ylabel('Ratio of bits exposed to string length')
plt.show()
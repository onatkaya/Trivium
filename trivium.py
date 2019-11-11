
"""
Created by Feyzi Ege Kumec (Sabanci University) and Onat Kaya (Sabanci University).

In the code below, a Python version of the stream cipher Trivium is implemented.
(To know more about Trivium, the paper published by De Canniere (KU Leuven) and Preneel (KU Leuven) could be checked out, which could be found in this repository.)

One of the most popular Python implementations that we found on the internet was created by Friedrich Wiemer (Ruhr-University Bochum). 
(Link: https://github.com/pfasante/trivium/blob/master/src/python/trivium.py).

Our solution has some differences from Wiemer's and we would like to explain what are these:

1) First of all, our code handles inputs, 80-bit key and 80-bit initial value, bitwise and there is no change in the order. In Wiener's approach
   the byte-wise approach is chosen, which implies that groupings are made of 8-bits. Afterward, the first bytes are moved to the end and the bits inside these groups are also reversed as well.

Example:

Input (in our approach): 0, 1, 2, ..., 79

Input (in Wiener's approach): 72-79, ..., 0-7   

2) When generating the keystream, we again handle the stream bitwise and do not change the order of the bits, we just print it the way it is.
   On the other hand, in Wiener's implementation, the bits of the keystream are grouped byte-wise again. While it does not send the first bytes to the end like in 1),
   it is reversing the order of the bits in each group.
   
Example (we assume that the keystream is 128 bits long):

Input (in our approach): 0, 1, 2, ..., 120, ..., 127

Input (in Wiener's approach): 7-0, ..., 127-120   

It is believed that, with our approach, the confusion about keeping track of the bits during trying out different test cases and debugging is going to be much simpler.

"""

import numpy as np
from collections import deque
from itertools import repeat
from sys import version_info

eighty_bit_input = "11111010101001110101010000000001101011100101101100001000101101010110001000001111"
initial_value_input = "11000111011000001111100110010010001010111100010001011101111101101000111100101000"

eighty_bit_key = []
initial_value = []

key_length_str = "128"

key_length = int(key_length_str) # str to int conversion

for m in range(0,80):
    eighty_bit_key.append(int(eighty_bit_input[m])) # Putting each bit to an array
    initial_value.append(int(initial_value_input[m])) # Putting each bit to an array
    
#creating the last portion of the initial state bits
last_initial_bits = np.append(np.zeros(108,dtype=int),[1,1,1]) ;
last_initial_bits = list(last_initial_bits) ;

#creating the zeros padded to the initial value and the key
first_zeros = np.zeros(13,dtype=int) ;
second_zeros = np.zeros(4,dtype=int) ;

#turning the zeros into a list
first_zeros = list(first_zeros) ;
second_zeros = list(second_zeros) ;

#appending the zeroes and turning the appended version to list again
first_93_bits = np.append(eighty_bit_key,first_zeros) ;
second_set_of_bits = np.append(initial_value,second_zeros) ;
first_93_bits = list(first_93_bits) ;
second_set_of_bits = list(second_set_of_bits) ;

#appending the first 177 bits and turning them into a list
first_177_bits = np.append(first_93_bits,second_set_of_bits) ;
first_177_bits = list(first_177_bits) ;

#appending the last bits and turning the whole thing into a list
initial_state_bits = np.append(first_177_bits,last_initial_bits) ;
initial_state_bits = list(initial_state_bits) ;

print("init#1:",initial_state_bits)

#initializing the intermediate bits noted by t
t = [0,0,0] ;


for k in range(4*288):

  t[0] = (initial_state_bits[65]) ^ ((initial_state_bits[90])&(initial_state_bits[91])) ^ (initial_state_bits[92]) ^ (initial_state_bits[170]) ;
  t[1] = (initial_state_bits[161]) ^ ((initial_state_bits[174])&(initial_state_bits[175])) ^ (initial_state_bits[176]) ^ (initial_state_bits[263]) ;
  t[2] = (initial_state_bits[242]) ^ ((initial_state_bits[285])&(initial_state_bits[286])) ^ (initial_state_bits[287]) ^ (initial_state_bits[68]) ;

  state_93 = np.append(t[2],initial_state_bits[0:92]) ;
  state_93 = list(state_93) ;

  state_94_177 = np.append(t[0],initial_state_bits[93:176]) ;
  state_94_177 = list(state_94_177) ;

  state_178_288 = np.append(t[1],initial_state_bits[177:287]) ;
  state_178_288 = list(state_178_288) ;

  state_new_bits = np.append(state_93,state_94_177) ;
  state_new_bits = np.append(state_new_bits,state_178_288) ;

  state_new_bits = list(state_new_bits) ;
  initial_state_bits = state_new_bits ;

print("init#2:",initial_state_bits)

#initialization is over, now writing code for key generation

index = 1 ;
z = np.zeros(key_length,dtype=int) ;

while(index<=key_length):
    t[0] = (initial_state_bits[65]) ^ (initial_state_bits[92]) ;
    t[1] = (initial_state_bits[161]) ^ (initial_state_bits[176]) ;
    t[2] = (initial_state_bits[242]) ^ (initial_state_bits[287]) ;
    
    z[index-1] = (t[0]) ^ (t[1]) ^ (t[2]) ;
    
    t[0] = (t[0]) ^ ((initial_state_bits[90]) & (initial_state_bits[91])) ^ (initial_state_bits[170]) ;
    t[1] = (t[1]) ^ ((initial_state_bits[174]) & (initial_state_bits[175])) ^ (initial_state_bits[263]) ;
    t[2] = (t[2]) ^ ((initial_state_bits[285]) & (initial_state_bits[286])) ^ (initial_state_bits[68]) ;
 
    state_93 = np.append(t[2],initial_state_bits[0:92]) ;
    state_93 = list(state_93) ;
    
    state_94_177 = np.append(t[0],initial_state_bits[93:176]) ;
    state_94_177 = list(state_94_177) ;
    
    state_178_288 = np.append(t[1],initial_state_bits[177:287]) ;
    state_178_288 = list(state_178_288) ;
    
    state_new_bits = np.append(state_93,state_94_177) ;
    state_new_bits = np.append(state_new_bits,state_178_288) ;
    
    state_new_bits = list(state_new_bits) ;
    initial_state_bits = state_new_bits ;

    index = index+1 ;
    
result_str = ""

#Converting the key stream array to a single string, in order to print it
for m in range(0, len(z)):
  result_str = result_str + str(z[m])

print("The key generated is: ", result_str)
    

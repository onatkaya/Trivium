## Description

Created by Feyzi Ege Kumec (Sabanci University) and Onat Kaya (Sabanci University).

In the code below, a Python version of the stream cipher Trivium is implemented.
(To know more about Trivium, the paper published by De Canniere (KU Leuven) and Preneel (KU Leuven) could be checked out, which could be found in this repository.)

One of the most popular Python implementations that we found on the internet was created by [Friedrich Wiemer (Ruhr-University Bochum)](https://github.com/pfasante/trivium/blob/master/src/python/trivium.py).

Our solution has some differences from Wiemer's and we would like to explain what are these:

1) First of all, our code handles inputs, 80-bit key and 80-bit initial value, bitwise and there is no change in the order. In Wiener's approach
   the byte-wise approach is chosen, which implies that groupings are made of 8-bits. Afterward, the first bytes are moved to the end and the bits inside these groups are also reversed as well.


**Example**:

Input (in our approach): 0, 1, 2, ..., 79

Input (in Wiener's approach): 72-79, ..., 0-7   

2) When generating the keystream, we again handle the stream bitwise and do not change the order of the bits, we just print it the way it is.
   On the other hand, in Wiener's implementation, the bits of the keystream are grouped byte-wise again. While it does not send the first bytes to the end like in 1),
   it is reversing the order of the bits in each group.
   
**Example (we assume that the keystream is 128 bits long):**

Keystream (in our approach): 0, 1, 2, ..., 120, ..., 127

Keystream (in Wiener's approach): 7-0, ..., 127-120   

It is believed that, with our approach, the confusion about keeping track of the bits during trying out different test cases and debugging is going to be much simpler.

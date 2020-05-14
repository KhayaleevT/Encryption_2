**Utility for encoding and decoding your text in vigenere or caesar
ciphers, also can hack caesar**  
Encoding and decoding using examples:  
`encode --input input.txt --output output.txt --cipher caesar(or vigenere) --key 5(or LEMON)`
  
`decode --input input.txt --output output.txt --cipher caesar(or vigenere) --key 5(or LEMON)`  
Auto input and output will be the terminal  
Can hack caesar encoded message. Using example:  
`hack_caesar --input input.txt --output output.txt --freqs frequencies.txt`  
where freqs is argument for file with serialized dictionary of character frequencies,  
by which hack correctness will be determined( non-required argument )  

freq_count function for counting character frequencies from your file   
Serialized character frequencies count from input file, put to the output file, the frequencies can be used  
for caesar hacking.  
Using example:  
`freq_count --input input.txt --output output.txt`
**Utility for encoding and decoding your text in vigenere, vernam or caesar
ciphers, also can hack caesar**  
Encoding and decoding using examples:  
`encrypt.py decode --input example_data/caesar_out.txt --output example_data/caesar_decode.txt --cipher caesar --key 3
`  
`decode --input example_data/vigenere_out.txt --output example_data/vigenere_decode.txt --cipher vigenere --key LEMON`  
Auto input and output will be the terminal  
Can hack caesar encoded message. Using example:  
`hack_caesar --input input.txt --output output.txt --freqs frequencies.txt`  
where freqs is argument for file with serialized dictionary of character frequencies,  
by which hack correctness will be determined( non-required argument )  

freq_count function for counting character frequencies from your file   
Serialized character frequencies count from input file, put to the output file, the frequencies can be used  
for caesar hacking.  
Using example:  
`encrypt.py freq_count --input Alice.txt --output frequencies.txt`
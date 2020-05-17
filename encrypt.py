import pickle
import argparse
import sys
from collections import Counter
from typing import Tuple, Dict, Union

"""
Encryption utility
"""
alphabets = [(ord('a'), ord('z')), (ord('а'), ord('я')), (ord(' '), ord('@')), (ord('['), ord('`')),
             (ord('{'), ord(''))]
"""
alphabets stored in pairs of first and last letter codes(Tuple[ord,ord])
"""


def upper_alpha(alpha: Tuple[int, int]) -> Tuple[int, int]:
    """
    Args:
       alpha:Tuple[int,int] -alphabet
    Returns:
       Tuple[int,int]- upper version of alphabet
    """
    return ord(chr(alpha[0]).upper()), ord(chr(alpha[1]).upper())


def _get_alpha(_chr: chr) -> Union[Tuple[int, int], None]:
    """
    Args:
       _chr: char
    Returns:
       Tuple[int,int] if chr has alphabet and None else
    """
    _ord = ord(_chr.lower())
    global alphabets
    for alpha in alphabets:
        if alpha[0] <= _ord <= alpha[1]:
            return (alpha[0], alpha[1]) if _chr.islower() else upper_alpha(alpha)
    return None


def is_letter(_chr: chr) -> bool:
    """
    Args:
       _chr:char
    Returns:
        bool: whether the _chr is a letter
    """
    _ord = ord(_chr.lower())
    global alphabets
    for alpha in alphabets[0:2]:
        if alpha[0] <= _ord <= alpha[1]:
            return True
    return False


def _same_alphabets(alpha1: Tuple[int, int], alpha2: Tuple[int, int]) -> bool:
    """
    Args:
       alpha1,alpha2-alphabets
    Returns:
       bool: whether the alpha1 and alpha2 represent same alphabets
    """
    return chr(alpha1[0]).lower() == chr(alpha2[0]).lower()


def _shift_ord(_chr: chr, shift: int, _alpha=None) -> chr:
    """
    Args:
        _chr:char
        shift:int
        _alpha:alphabet of _chr if already known
    Returns:
        chr: char shifted on shift in its alphabet or the same chr if chr is not in alphabet
    """
    if shift == 0:
        return _chr
    if _alpha is None:
        _alpha = _get_alpha(_chr)
    numb = ord(_chr)
    if _alpha:
        numb = numb - _alpha[0]
        numb = _alpha[0] + (numb + shift) % (_alpha[1] + 1 - _alpha[0])
        return chr(numb)
    return _chr


def _caesar(file, key: int) -> str:
    """
    Args:
         file: text to be encoded
         key(int): key
    Returns:
          str: encoded text
    """
    ans = []
    for line in file:
        for ch in line:
            ans.append(_shift_ord(ch, key))
    return ''.join(ans)


MIN_ORD = 32


def _vernam_xor(ch: chr, xor_ch: chr) -> chr:
    """
    Args:
        ch,xor_ch -chars to be xored
    Returns:
        xor of two chars ords for vernam encoding
    """
    xor_1 = ord(ch) - MIN_ORD
    xor_2 = ord(xor_ch) - MIN_ORD
    return chr((xor_1 ^ xor_2) + MIN_ORD)


def _vernam(file, key: str) -> str:
    """
       Args:
            file: text to be encoded
            key(str): key, should be at least the size of encoding file
       Returns:
             str: encoded text
    """
    ans = []
    ch_num = 0
    for line in file:
        for ch in line:
            if ord(ch) < MIN_ORD:
                ans.append(ch)
                continue
            _shift_chr = key[ch_num]
            ch_num += 1
            ans.append(_vernam_xor(ch, _shift_chr))
    return ''.join(ans)


def _vigenere(file, key: str, _cipher: int = 1) -> str:
    """
       Args:
            file: text to be encoded
            key(str): key
            _cipher: should be 1 or -1 , 1 means encoding, -1 means decoding
       Returns:
             str: encoded text
    """
    ans = []
    ch_num = 0
    for line in file:
        for ch in line:
            ch_alpha = _get_alpha(ch)
            if ch_alpha:
                _shift_chr = key[ch_num % len(key)]
                ch_num += 1
                _shift_alpha = _get_alpha(_shift_chr)
                if _shift_alpha:
                    ans.append(_shift_ord(ch, _cipher * (ord(_shift_chr) - _shift_alpha[0]), ch_alpha))
                else:
                    ans.append(ch)
            else:
                ans.append(ch)
    return ''.join(ans)


def vernam_encode(file, key: str) -> str:
    return _vernam(file, key)


def vernam_decode(file, key: str) -> str:
    return _vernam(file, key)


def caesar_decode(file, key: int) -> str:
    return _caesar(file, -key)


def caesar_encode(file, key: int) -> str:
    return _caesar(file, key)


def vigenere_encode(file, key: str) -> str:
    return _vigenere(file, key)


def vigenere_decode(file, key: str) -> str:
    return _vigenere(file, key, -1)


def _first_file_letters(file, shift: int = 0, _max_amount: int = 40000):
    """
    Args:
        file
        shift(int)
        _max_amount(int)
    40000 is just random big number,you can put 1000000 or 500000 here as well
    the function is generator giving first max_amount file letters shifted on shift
    """
    _processed = 0
    for line in file:
        for _ch in line:
            shift_ch = _shift_ord(_ch, shift)
            if is_letter(shift_ch):
                yield shift_ch
                _processed += 1
        if _processed > _max_amount:
            break


def _frequencies(file) -> Dict[chr, float]:
    """
    Returns:
        Dict[chr,float]: dictionary of average chr frequencies in first 40000 file symbols
    """
    _letters = dict()
    _letters = Counter(_ch for _ch in _first_file_letters(file))
    data_amount = sum(_letters.values())
    for ch in _letters:
        _letters[ch] /= data_amount
    return _letters


def _dump_frequencies(freqs, _file='frequencies.txt'):
    with open(_file, 'wb') as fr:
        pickle.dump(freqs, fr)


def _load_frequencies(_file='frequencies.txt'):
    with open(_file, 'rb') as fr:
        return pickle.load(fr)


def _freq_diff(freqs1: Dict[chr, float], freqs2: Dict[chr, float]) -> float:
    """
    Args:
        freqs1(Dict[chr,float]),
        freqs2(Dict[chr,float]):dictionaries of character frequencies
    Returns:
        float: vector distance between freqs1 and freqs2
    """
    diff = 0
    for _alpha in alphabets[0:2]:
        for i in range(_alpha[0], _alpha[1] + 1):
            _chr = chr(i)
            freq1 = freqs1[_chr] if _chr in freqs1 else 0
            freq2 = freqs2[_chr] if _chr in freqs2 else 0
            diff += ((freq1 - freq2) ** 2)
    return diff


def _caesar_count_freq(file, key: int) -> Dict[chr, float]:
    """
    Counts character frequencies if file would be encoded with key, does not actually encode anything
    Args:
        file
        key(int)
    Returns:
         Dict[chr,float]:frequencies of text if encoded in caesar with the key
    """
    ans = Counter(_ch for _ch in _first_file_letters(file, key))
    let_amount = sum(ans.values())
    for ch in ans:
        ans[ch] /= let_amount
    file.seek(0)
    return ans


def caesar_hack(file, freqs: Dict[chr, float]) -> str:
    """
    Try to choose the most realistic looking key due to the average character
    frequencies and hack the caesar encoded text
    Args:
      file: text to try to decode
      freqs(Dict[chr,float]): frequencies dictionary
    Returns:
        str:supposed version of decoded text
    """
    best_key = min((_freq_diff(_caesar_count_freq(file, -key), freqs), key) for key in range(0, 33))[1]
    return caesar_decode(file, best_key)


def _encode(args):
    """
    Encoding processing
    :param args: args from terminal input
    """
    _input = _get_input_and_ready_output(args)
    cipher, key = _get_cipher_and_key(args)
    if cipher == "caesar":
        print(caesar_encode(_input, int(key)), end='')
    elif cipher == "vigenere":
        print(vigenere_encode(_input, key), end='')
    elif cipher == "vernam":
        print(vernam_encode(_input, key), end='')


def _decode(args):
    """
    Decoding processing
    :param args: args from terminal input
    """
    _input = _get_input_and_ready_output(args)
    cipher, key = _get_cipher_and_key(args)
    if cipher == "caesar":
        print(caesar_decode(_input, key), end='')
    elif cipher == "vigenere":
        print(vigenere_decode(_input, key), end='')
    elif cipher == "vernam":
        print(vernam_decode(_input, key), end='')


def _get_input_and_ready_output(args):
    """
    Output and input processing
    :param args: args from terminal input
    Returns:
    text input to process later
    """
    if args.output:
        sys.stdout = open(args.output, 'w', encoding='utf-8')
    _input = open(args.input, 'r', encoding='utf-8') if args.input else sys.stdin
    return _input


CIPHERS = {"vigenere", "caesar", "vernam"}


def _get_cipher_and_key(args):
    """
    Getting cipher and key from args
    :param args: args from terminal input
    Returns:
    tuple:pair of cipher and key
    """
    cipher = args.cipher
    if cipher is None or cipher not in CIPHERS:
        cipher = "caesar"
    key = args.key
    if key is None:
        key = "1" if cipher == "caesar" else "LEMON"
    if cipher == "caesar":
        key = int(key) if key.isdigit() else 1
    return cipher, key


def freq_count(args):
    """
    Frequencies count processing
    :param args: args from terminal input
    """
    _input = _get_input_and_ready_output(args)
    _output = args.output if args.output else 'frequencies.txt'
    _dump_frequencies(_frequencies(_input), _output)


def hack(args):
    """
    Caesar encoded text hacking processing
    :param args: args from terminal input
    """
    _input = _get_input_and_ready_output(args)
    _freqs = _load_frequencies(args.freqs) if args.freqs else _load_frequencies()
    print(caesar_hack(_input, _freqs), end='')


def parse_args():
    parser = argparse.ArgumentParser(description='Encryption utility')
    subparsers = parser.add_subparsers()
    parser_encode = subparsers.add_parser('encode')
    parser_encode.add_argument('--input', type=str, help="text to encode")
    parser_encode.add_argument('--output', type=str, help="where to put encoded text")
    parser_encode.add_argument('--cipher', type=str, help="cipher used to encode text")
    parser_encode.add_argument('--key', help="key to encode text with")
    parser_encode.set_defaults(func=_encode)
    parser_decode = subparsers.add_parser('decode')
    parser_decode.add_argument('--input', type=str, help="text to decode")
    parser_decode.add_argument('--output', type=str, help="where to put decoded text")
    parser_decode.add_argument('--cipher', type=str, help="cipher used to encode text")
    parser_decode.add_argument('--key', help="key used to encode text")
    parser_decode.set_defaults(func=_decode)
    parser_freq = subparsers.add_parser('freq_count')
    parser_freq.add_argument('--input', type=str, help="text to count frequency of letters")
    parser_freq.add_argument('--output', help="where to put list of frequencies")
    parser_freq.set_defaults(func=freq_count)
    parser_hack = subparsers.add_parser('hack_caesar')
    parser_hack.add_argument('--input', type=str, help="file trying to hack")
    parser_hack.add_argument('--output', type=str, help="where to put decoded text")
    parser_hack.add_argument('--freqs', type=str, help="file with serialized dictionary of frequencies")
    parser_hack.set_defaults(func=hack)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


main()

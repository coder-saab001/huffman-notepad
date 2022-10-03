import json
class node:
    def __init__(self, freq, symbol, left = None, right = None):
        # Frequency of symbol
        self.freq = freq

        # Symbol itself
        self.symbol = symbol

        # left node
        self.left = left
        
        # Right node
        self.right = right

        # Tree Direction 
        self.huff = ''

dict = {} # Mapping each character to its corresponding huffman codes
reverseDict = {} # Mapping huffman codes to each corresponding charater

## Recursive function to get huffman codes corresponding to each character
def printNodes(node, val = ''):
    newVal = val + str(node.huff)

    if node.left is not None:
        printNodes(node.left, newVal)

    if node.right is not None:
        printNodes(node.right, newVal)

    if node.left is None and node.right is None:
        dict[node.symbol] = newVal
        reverseDict[newVal] = node.symbol

## Encoding the given string to corresponding huffman codes
def getEncodedText(originalText):
    encodedText = ""
    for i in originalText:
        encodedText = encodedText + dict[i]
    return encodedText

## Adding padding at last so at to make the length of encoded string a multiple of 8
## Also adding the length of padding aaded in front in 8-bits format only
def getPaddedEncodedText(encodedText):
    extra_padding = 8 - len(encodedText) % 8
    for i in range(0, extra_padding):
        encodedText += "0"
    padded_info = "{0:08b}".format(extra_padding)
    encodedText = padded_info + encodedText
    return encodedText

## Converting each set to 8-bits to its corresponding byte character
def getByteArray(paddedEncodedText):
    b = bytearray()
    for i in range(0, len(paddedEncodedText), 8):
        byte = paddedEncodedText[i:i+8]
        b.append(int(byte, 2))
    return b

## Function called by main file providing string data to encode 
## Return decoded string and reverseDict codes
def encode(originalText):
    freq = {}
    originalText = originalText.rstrip()

    # Grenerating freq map
    for i in originalText:
        freq[i] = 0
    for i in originalText:
        freq[i] = freq[i] + 1

    generateHuffmanCodes(freq)
    encodedText = getEncodedText(originalText)
    paddedEncodedText = getPaddedEncodedText(encodedText)
    byteArray = getByteArray(paddedEncodedText)

    return reverseDict, byteArray

## Function creating huffman tree and further calling printNodes to create huffman codes map
def generateHuffmanCodes(freq):
    nodes = []
    for i in freq:
        nodes.append(node(freq[i], i))
    while len(nodes) > 1:
        nodes = sorted(nodes, key = lambda x:x.freq)

        left = nodes[0]
        right = nodes[1]

        left.huff = 0
        right.huff = 1

        newNode = node(left.freq + right.freq, '#', left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
    
    ## Huffman Tree is ready
    if(len(nodes) > 0):
        printNodes(nodes[0])

## Function extracting padding length and removing it
def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1*extra_padding]
    return encoded_text

## Decoding to the original text from the encoded binar string and reverse mapping
def decode_text(encoded_text, reverse_mapping):
    current_code = ""
    decoded_text = ""
    for bit in encoded_text:
        current_code += bit
        if(current_code in reverse_mapping):
            character = reverse_mapping[current_code]
            decoded_text += character
            current_code = ""
    return decoded_text

## Function decoding the encoded byte_string and reverse_mapping to the original text yooo
def decode(byte_string, reverse_mapping):
    # Converting the byte string to the corresponding binary string
    bit_string = ""
    for byte in byte_string:
        bits = bin(byte)[2:].rjust(8, '0')
        bit_string += bits
    encoded_text = remove_padding(bit_string)
    decompressed_text = decode_text(encoded_text, reverse_mapping)
    return decompressed_text

    


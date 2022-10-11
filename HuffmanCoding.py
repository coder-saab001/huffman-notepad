import json
class node:
    def __init__(self, freq, symbol, left = None, right = None)
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

dict = {} 
reverseDict = {}

def printNodes(node, val = ''):
    newVal = val + str(node.huff)

    if node.left is not None:
        printNodes(node.left, newVal)

    if node.right is not None:
        printNodes(node.right, newVal)

    if node.left is None and node.right is None:
        dict[node.symbol] = newVal
        reverseDict[newVal] = node.symbol

def getEncodedText(originalText):
    encodedText = ""
    for i in originalText:
        encodedText = encodedText + dict[i]
    return encodedText

def getPaddedEncodedText(encodedText):
    extra_padding = 8 - len(encodedText) % 8
    for i in range(0, extra_padding):
        encodedText += "0"
    padded_info = "{0:08b}".format(extra_padding)
    encodedText = padded_info + encodedText
    return encodedText

def getByteArray(paddedEncodedText):
    b = bytearray()
    for i in range(0, len(paddedEncodedText), 8):
        byte = paddedEncodedText[i:i+8]
        b.append(int(byte, 2))
    return b

def encode(originalText):
    freq = {}
    originalText = originalText.rstrip()

    for i in originalText:
        freq[i] = 0
    for i in originalText:
        freq[i] = freq[i] + 1

    generateHuffmanCodes(freq)
    encodedText = getEncodedText(originalText)
    paddedEncodedText = getPaddedEncodedText(encodedText)
    byteArray = getByteArray(paddedEncodedText)

    return reverseDict, byteArray

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

    if(len(nodes) > 0):
        printNodes(nodes[0])

def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1*extra_padding]
    return encoded_text

def decode_text(encoded_text, reverse_mapping):
    current_code = ""
    decoded_text = ""
    for bit in encoded_text:
        current_code += bit
        if(current_code in reverse_mapping):
            character = reverse_mapping[current_code]
            decoded_text += character
            current_code = " "
    return decoded_text

def decode(byte_string, reverse_mapping):
    bit_string = ""
    for byte in byte_string:
        bits = bin(byte)[2:].rjust(8, '0')
        bit_string += bits
    encoded_text = remove_padding(bit_string)
    decompressed_text = decode_text(encoded_text, reverse_mapping)
    return decompressed_text

    


def extract_substring(message, offset, length):
    message = message.replace('\n', ' \n')
    return message[offset:offset + length]


message = ''
offset = 419
length = 14

if __name__ == '__main__':
    substring = extract_substring(message, offset, length)
    print(f"Extracted substring: {substring}")

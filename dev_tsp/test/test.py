import base64

# base64解码并写入文件
encoded_data = 'ASgb01ToD1A5+tPBbt603ce/T0oMgUADoKQx0nJA70AAcUwNk7j17Cguc0AMUkggmngDjP3aiXsakbjqOKBiE4Bx3pm6nFhxgUwlc0ACE9RSmTPy5oooAiDgdDknpTCwBxyaKKQz'

if __name__ == '__main__':
    decoded_data = base64.b64decode(encoded_data)
    print(decoded_data)
    file_path = 'output_file'
    with open(file_path, 'wb') as file:
        file.write(decoded_data)

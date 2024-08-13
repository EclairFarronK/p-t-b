def extract_substring(message, offset, length):
    return message[offset:offset + length]


# 87
# 示例消息
message = ''
print(len(message))
# 示例偏移量和长度
offset = 32
length = 28

# 提取子字符串
substring = extract_substring(message, offset, length)

print(f"Extracted substring: {substring}")

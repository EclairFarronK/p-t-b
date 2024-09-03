import re


def extract_abc(text):
    # 正则表达式，匹配 [a--b](c) 的模式
    pattern = r'([📢👥])\[(.*?)\-\-(.*?)\]\(https?://t\.me/(.*?)\)'

    # 使用 findall 方法查找所有匹配项，并生成列表
    matches = re.findall(pattern, text)

    # 将所有匹配项添加到一个大列表中
    result = [list(match) for match in matches]
    return result


# 示例字符串
text = ''

# 提取并打印结果
result = extract_abc(text)
print(result)

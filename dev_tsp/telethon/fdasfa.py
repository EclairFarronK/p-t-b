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
text = "**[推广]** [✅包赢计划回血上岸日赚20万🔥18年专业团队保驾护航](https://t.me/caipiao64)1.📢[街拍偷拍高抄抄底洗澡更衣--35.0K](https://t.me/Jiepa)2.📢[街拍/偷拍/露出/抄底/高抄/厕拍/调教/写真--11.0K](https://t.me/jikeful)3.👥[街拍偷拍高抄抄底洗澡更衣--8.6K](https://t.me/Jiepaaa)"

# 提取并打印结果
result = extract_abc(text)
print(result)

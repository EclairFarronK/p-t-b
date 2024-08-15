import re


# todo 测试除了导入md文件还能导入其他文件吗？
def scan_links_from_md(file_path):
    # /后遇到 )]?/\n结束
    # 排除joinchat和*bot
    pattern = r'https?://t\.me/((?!joinchat)(?!.*bot)[^ )\]?/\n]+)'
    # 读取Markdown文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 使用正则表达式查找所有匹配的链接
        usernames = re.findall(pattern, content, re.IGNORECASE)
    return list(set(usernames))


if __name__ == '__main__':
    links = scan_links_from_md('../README.md')
    # todo 将数据导入到MongoDB中去

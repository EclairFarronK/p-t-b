def extract_substring(message, offset, length):
    return message[offset:offset + length]


# 87
# 示例消息
message = "🌐✅球速体育代理佣金70%、菲亚博系u存u提每日提款无上限\n\n🌐🔥飞鸟VPN加速器🔥免费试用官方推荐、视频秒开无限流量🔥\n\n👥你好交流群 18k\n👥祝你好运 6"
print(len(message))
# 示例偏移量和长度
offset = 32
length = 28

# 提取子字符串
substring = extract_substring(message, offset, length)

print(f"Extracted substring: {substring}")

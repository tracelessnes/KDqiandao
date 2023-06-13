import re

# 假设 rep 是请求返回的响应对象
text = rep.text

# 使用正则表达式提取需要的文本内容
match = re.search(r'<div\s+id="messagetext"\s+class="(alert_right|alert_error)">\s*<p>(打卡成功.*?)</p>', text, flags=re.DOTALL)

if match:
    result = match.group(2)
    print(result)
else:
    print('未找到目标文本')
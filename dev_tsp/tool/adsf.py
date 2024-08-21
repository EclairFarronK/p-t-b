import re

regex = '11?23'
print(re.match(regex, '23'))
print(re.findall(regex, '1123'))
print(re.findall(regex, '1234'))
print(re.findall(regex, '121'))
print(re.findall(regex, '123'))

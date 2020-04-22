import subprocess

#方法一：进入某个环境执行语句（adb shell），注意shell内部命令需要带\n，执行完后一定记得执行exit命令退出，否则会阻塞
obj = subprocess.Popen(['adb', 'shell'], shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
obj.stdin.write('ls\n'.encode('utf-8'))
obj.stdin.write('exit\n'.encode('utf-8'))  #重点，一定要执行exit
info,err = obj.communicate()
print(info.decode('gbk'))
print(err.decode('gbk'))

#方法二：进入某个环境执行语句（adb shell）,命令用列表方式全部列出
cmds = [
    "cd data",
    'cd data',
    "ls",
    "exit",#这是是非常关键的，退出
]
obj = subprocess.Popen("adb shell", shell= True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
info = obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'));
for item in info:
    if item:
        print(item.decode('gbk'))
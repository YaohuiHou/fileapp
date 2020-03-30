# fileapp
electron-vue 实现手机文件管理—— 文件助手


window 打包
```
npm run win32
# or
npm run win64
```

Mac 打包
```
npm run mac
```

其中--platform是配置打包成什么平台的安装文件，下面是可选的值

- win系统： win或者win32，即--platform=win或者--platform=win32
- mac系统：mac或者darwin，即--platform=mac或者--platform=darwin
- Linux系统：linux， 即--platform=linux
- 所有平台：all， 即--platform=all

其中--arch是指定系统是什么架构的，常见的例如32位和64位操作系统，这个参数的可选值有

- ia32， 即--arch=ia32， 32位操作系统，也可以在64位操作系统中安装
- x64， 即--arch=x64， 64位操作系统，使用本架构打包无法再32位操作系统中安装
- armv7l， 即--arch=armv7l， 使用比较少
- arm64， 即--arch=arm64， 使用比较少
- 参数--platform和--arch已经被标志为过期，新的写法如下
```
electron-builder --win --x64
electron-builder --win --ia32
electron-builder --win --armv7l
```
如果--platform和--arch两个参数都没有指定，那么在打包的时候会参考当前操作系统的架构和平台进行打包，也就是说，以下命令如果在不同的操作系统上运行结果也是不一样的

```
electron-builder
```

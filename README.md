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

Linux 打包

```
npm run linux
```

其中--platform 是配置打包成什么平台的安装文件，下面是可选的值

- win 系统： win 或者 win32，即--platform=win 或者--platform=win32
- mac 系统：mac 或者 darwin，即--platform=mac 或者--platform=darwin
- Linux 系统：linux， 即--platform=linux
- 所有平台：all， 即--platform=all

其中--arch 是指定系统是什么架构的，常见的例如 32 位和 64 位操作系统，这个参数的可选值有

- ia32， 即--arch=ia32， 32 位操作系统，也可以在 64 位操作系统中安装
- x64， 即--arch=x64， 64 位操作系统，使用本架构打包无法再 32 位操作系统中安装
- armv7l， 即--arch=armv7l， 使用比较少
- arm64， 即--arch=arm64， 使用比较少
- 参数--platform 和--arch 已经被标志为过期，新的写法如下

```
electron-builder --win --x64
electron-builder --win --ia32
electron-builder --win --armv7l
```

如果--platform 和--arch 两个参数都没有指定，那么在打包的时候会参考当前操作系统的架构和平台进行打包，也就是说，以下命令如果在不同的操作系统上运行结果也是不一样的

```
electron-builder
```

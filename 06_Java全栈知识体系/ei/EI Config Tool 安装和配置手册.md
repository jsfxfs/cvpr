# EI Config Tool 安装和配置手册

> 本文主要包含EI Config Tool的安装部署和配置手册等。

## 配置介绍

> 包含部署的结构和一些集成的配置。

### 部署结构

- web前端
  - Vue + Ant Design Pro - 前端页面
  - Springboot - 支撑前端的API和后台服务
  - 将上述两部分打包至jar中，所以只有一个jar文件
- 后端
  - C++相关服务
- 数据解耦
  - xml文件
  - C++后端可以提供一些即时数据交互的接口

本文主要包含web服务的部署和配置。

### 一些配置

> 相关配置介绍和配置位置，可以看下文场景。

相关配置的参数可以添加在 java -jar 命令的后方, 比如linux下的执行脚本：

`java -jar $3 --server.port=9999 --eiconfig.init-xml-path=/opt/EIConfig.xml`

#### xml的配置加载的问题

- 如何在程序启动时加载指定的默认的xml文件？

程序中给定了`eiconfig.init-xml-path`配置参数，这个参数主要用来指定程序启动时默认加载的EI Config的xml文件，这个配置是**服务器上**存放的xml文件的**全路径**。

如果设置了这个参数，程序在启动时会尝试默认加载这个文件。

- 是否可以在界面上指定xml并进行加载？

可以，已经在界面上方已经实现了相关功能。输入xml全路径，然后点击Load即可完成加载。

![](https://www.pdai.tech/images/eiconfig/ei-install-5.png)

#### 修改后保存配置的问题

- 当配置更改后如何保存到xml文件中？

界面上方添加了Save按钮，在修改配置后点Save，会保存xml至输入的全路径中；

路径的上层文件夹必须是服务器上已经存在的，以防止服务器注入攻击；

路径后面的xml文件名既可以是新的文件名也可以是初始化的已经存在的文件名，如果是新的文件名，会生成新的xml文件，类似备份操作，如果已经存在的文件名，会重新覆盖文件内容。

- 当配置修改后，如果重启C++后台的服务呢？

程序中给定了`eiconfig.cmd-when-save-file`的配置参数，如果指定，可以在保存配置文件时自动执行给定的脚本，比如`service xxx restart`。

- 当配置修改后，能否自动保存至xml文件呢？

可以，程序中给定了`eiconfig.auto-save-xml-file-when-update`配置参数，默认是false。虽然提供了参数，但是在同时设置了`eiconfig.cmd-when-save-file`参数时，并不推荐设置为true，因为每次更新操作都会重新执行给定脚本。

## Windows 平台安装和配置

> windows平台的安装基于.NET4 和Java环境，所以需要先检查相关环境。

### 环境检查

- 检查是否安装jdk, 如果没有的话去官网下载JDK进行安装；在cmd 输入`java -version`，如果返回Java版本号，即表示已经安装了jdk。通常我们的CAT机都会预装JDK环境的。

```bash
C:\Users\Z003MRZB>java -version
java version "1.8.0_65"
Java(TM) SE Runtime Environment (build 1.8.0_65-b17)
Java HotSpot(TM) 64-Bit Server VM (build 25.65-b01, mixed mode)
```

- 检查是否有.NET 4的环境

windows大多是自带了.NET 。

### 安装和运行

- 获得如下三个安装文件，（蓝色背景的三个，其它是运行之后的日志文件和启动脚本，由于启动脚本对windows环境有一定的依赖，所以你可以不用脚本安装）

![](https://www.pdai.tech/images/eiconfig/ei-install-1.png)

- 安装EIConfig服务, 这里我的目录是`C:\Users\Z003MRZB\Desktop\ei\`

通过cmd 运行 `目录\eiconfig.exe install`

```bash
C:\Users\Z003MRZB>C:\Users\Z003MRZB\Desktop\ei\eiconfig.exe install
2020-09-20 15:22:59,614 INFO  - Installing the service with id 'EIConfig'
```

上述操作，表示我在window中安装了一个EIConfig的服务。

- 启动EIConfig服务

打开服务管理

![](https://www.pdai.tech/images/eiconfig/ei-install-2.png)

启动服务

![](https://www.pdai.tech/images/eiconfig/ei-install-3.png)

过1分钟以后，打开网页http://localhost:9999

![](https://www.pdai.tech/images/eiconfig/ei-install-4.png)

### 卸载EIConfig

- 同上一步，stop EIConfig
- cmd 下执行uninstall命令

```bash
C:\Users\Z003MRZB>C:\Users\Z003MRZB\Desktop\ei\eiconfig.exe uninstall
2020-09-20 16:08:38,409 INFO  - Uninstalling the service with id 'EIConfig'
```

### 版本更新

后续可能还会涉及到功能的更新

- 只需要替换jar包，然后重启EIConfig即可。

## Linux 平台安装和配置

> 我们制作一个eiconfig-web的服务，这样我们可以使用标准的服务方式进行`status/start/stop/restart`（不同Linux环境略有差别，比如centos7可以用`systemctl start eiconfig-web`)；并且设置为开机自启动。

### 安装文件拷贝

- 在`/opt`下创建`EIConfig`文件夹，将如下内容拷贝至这个文件夹

  - bin/eiconfig.jar - 这个是web服务，包含了web的前后端
  - eiconfig - 这个是启动脚本，**启动参数配置在这个文件中**
- 在`/var/log`下创建`/EIConfig/process`文件夹

  - 程序处理的日志会保存到这里
- 将如下文件拷贝至`/etc/init.d`这个文件夹

  - eiconfig-web - 这个就是我们自定义的服务, 包含了`status/start/stop/restart`服务命令

### 服务配置和启动

- 赋予权限

```bash
sudo chmod 777 /etc/init.d/eiconfig-web
```

- 启动服务

```bash
sudo service eiconfig-web start
```

- 开机自启

```bash
chkconfig --list
chkconfig eiconfig-web on
```

- 查看端口, 服务默认绑定在9999端口

```bash
netstat -nltp
```

- 查看防火墙，不要屏蔽了

```bash
systemctl status firewalld
```

### 版本更新

后续可能还会涉及到功能的更新

- 只需要替换bin下的jar包，然后重启eiconfig-web即可。
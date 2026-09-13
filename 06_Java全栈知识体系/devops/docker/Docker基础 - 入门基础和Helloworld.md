# Docker基础 - 入门基础和Helloworld

> 在了解了虚拟化技术和Docker之后，让我们上手Docker，看看Docker是怎么工作的。这里会介绍CentOS环境下Docker的安装和配置，以及会给你展示两个实例，给你一个直观的理解。再啰嗦下，有条件的情况下直接看[官网](https://docs.docker.com/install/linux/docker-ce/centos/), 网上资料鱼龙混杂，版本也更新不及时。@pdai

## Docker 架构

> 理解如下的一些概念，你才知道安装什么

Docker 使用客户端-服务器 (C/S) 架构模式，使用远程API来管理和创建Docker容器。

- **Docker 客户端(Client)** : Docker 客户端通过命令行或者其他工具使用 Docker SDK (https://docs.docker.com/develop/sdk/) 与 Docker 的守护进程通信。
- **Docker 主机(Host)** ：一个物理或者虚拟的机器用于执行 Docker 守护进程和容器。

Docker 包括三个基本概念:

- **镜像（Image）**：Docker 镜像（Image），就相当于是一个 root 文件系统。比如官方镜像 ubuntu:16.04 就包含了完整的一套 Ubuntu16.04 最小系统的 root 文件系统。
- **容器（Container）**：镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中的类和实例一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。
- **仓库（Repository）**：仓库可看着一个代码控制中心，用来保存镜像。

![](https://www.pdai.tech/images/devops/docker/docker-x-1.png)

## Docker 安装

> 从 2017 年 3 月开始 docker 在原来的基础上分为两个分支版本: Docker CE 和 Docker EE：Docker CE 即社区免费版；Docker EE 即企业版，强调安全，但需付费使用；按照官网上Docker Engine - Community包现在就是叫做Docker CE。这里将展示在CentOS上安装Docker。

### CentOS 版本要求

官网要求，使用CentOS7的稳定版本，同时：

- 启用`centos-extras`
- 推荐使用`overlay2`存储驱动

### 卸载老的Docker及依赖

> 为什么你可能还需要删除较低的Docker安装？因为较旧版本的Docker被称为docker或docker-engine（它是一个简化Docker安装的命令行工具，通过一个简单的命令行即可在相应的平台上安装Docker，比如VirtualBox、 Digital Ocean、Microsoft Azure）

```bash
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

### 安装一些依赖库

- yum-utils 提供 yum-config-manager 类库
- device-mapper-persistent-data 和 lvm2 被devicemapper 存储驱动依赖

```bash
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
```

设置稳定版本的库

```bash
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

### 安装Docker CE

```bash
yum install -y docker-ce
```

安装完之后启动

```bash
sudo systemctl start docker
```

测试是否安装成功

```bash
[root@pdai ~]# systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled; vendor preset: disabled)
   Active: active (running) since Mon 2020-02-17 13:57:45 CST; 39s ago
     Docs: https://docs.docker.com
 Main PID: 26029 (dockerd)
    Tasks: 8
   Memory: 36.9M
   CGroup: /system.slice/docker.service
           └─26029 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd
```

## 仓库配置

> Docker 安装好以后，我们就要开始为拉取镜像准备了；国内从 DockerHub 拉取镜像有时会特别慢，此时可以**配置镜像加速器**。

Docker 官方和国内很多云服务商都提供了国内加速器服务，比如：

- 阿里云的加速器：https://help.aliyun.com/document_detail/60750.html
- 网易加速器：http://hub-mirror.c.163.com
- Docker官方中国加速器：https://registry.docker-cn.com
- ustc 的镜像：https://docker.mirrors.ustc.edu.cn
- daocloud：https://www.daocloud.io/mirror#accelerator-doc（注册后使用）

**这里配置 Docker官方中国的加速器**：

对于使用 systemd 的系统，请在 /etc/docker/daemon.json 中写入如下内容（如果文件不存在请新建该文件）

```bash
{"registry-mirrors":["https://registry.docker-cn.com"]}
```

之后重新启动服务

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

## 镜像查看和拉取

> 拉一个docker镜像试试吧？

拉取hello world

```bash
[root@pdai ~]# docker pull hello-world:latest
latest: Pulling from library/hello-world
1b930d010525: Pull complete
Digest: sha256:9572f7cdcee8591948c2963463447a53466950b3fc15a247fcad1917ca215a2f
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
```

看本地仓库是否有这个库

```bash
[root@pdai ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              fce289e99eb9        13 months ago       1.84kB
```

运行这个镜像的实例，即容器

```bash
[root@pdai ~]# docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

> 注意, 如果你在没有镜像的时候，直接`docker run hello-world`也是可以的；它会先检查本地是否有这个镜像，没有的话会先从指定仓库中拉取。

## 容器实例-ubuntu实例

> 上面我们跑了一个官方的Hello-world容器实例, 这里通过介绍运行ubuntu的实例来全面理解如何跑一个Docker实例

### 从一个ubuntu的hello world说起

Docker 允许你在容器内运行应用程序， 使用 docker run 命令来在容器内运行一个应用程序。这里同样是个Hello World，不同在于它是在容器内部运行的。

```bash
[root@pdai ~]# docker run ubuntu:latest /bin/echo "Hello world"
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
5c939e3a4d10: Pull complete
c63719cdbe7a: Pull complete
19a861ea6baf: Pull complete
651c9d2d6c4f: Pull complete
Digest: sha256:8d31dad0c58f552e890d68bbfb735588b6b820a46e459672d96e585871acc110
Status: Downloaded newer image for ubuntu:latest
Hello world
```

我们看下各个参数的含义：

- `docker`: Docker 的二进制执行文件。
- `run`: 与前面的 docker 组合来运行一个容器。
- `ubuntu:latest` 指定要运行的镜像，Docker 首先从本地主机上查找镜像是否存在，如果不存在，Docker 就会从镜像仓库 Docker Hub 下载公共镜像。
- `/bin/echo "Hello world"`: 在启动的容器里执行的命令

以上命令完整的意思可以解释为：Docker 以 ubuntu 最新的（默认是latest) 镜像创建一个新容器，然后在容器里执行 bin/echo "Hello world"，然后输出结果。

### 运行交互式的容器

> 以上面例子，容器跑的是Ubuntu是一个系统实例，能否进入系统进行交互呢？

我们通过 docker 的两个参数 -i -t，让 docker 运行的容器实现"对话"的能力：

```bash
[root@pdai ~]# docker run -i -t ubuntu:latest
root@414bf796cbe4:/# echo 'hello world'
hello world
root@414bf796cbe4:/#
```

各个参数解析：

- `-t`: 在新容器内指定一个伪终端或终端。
- `-i`: 允许你对容器内的标准输入 (STDIN) 进行交互。

我们可以通过运行 exit 命令或者使用 CTRL+D 来退出容器

```bash
root@414bf796cbe4:/# exit
exit
[root@pdai ~]#
```

### 运行容器至后台模式

> 我们先来看, 当我们跑完上面例子之后，我们看下后台是否有docker容器实例？

显然没有任何容器实例

```bash
[root@pdai ~]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

所以我们需要`-d`参数，来让容器实例在后台运行，比如：

```bash
[root@pdai ~]# docker run -d ubuntu:latest /bin/sh -c "while true; do echo hello world; sleep 1; done"
1a51d2f023c947f2be2d9a78eb863e854ca302c89bf354654c409e23e7dd25d7
```

在输出中，我们没有看到期望的 "hello world"，而是一串长字符

```bash
2b1b7a428627c51ab8810d541d759f072b4fc75487eed05812646b8534a2fe63
```

这个长字符串叫做容器 ID，对每个容器来说都是唯一的，我们可以通过容器 ID 来查看对应的容器发生了什么。

首先，我们需要确认容器有在运行，可以通过 docker ps 来查看：

```bash
[root@pdai ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
1a51d2f023c9        ubuntu:latest       "/bin/sh -c 'while t…"   About a minute ago   Up About a minute                       gifted_brown
```

输出详情介绍：

- CONTAINER ID: 容器 ID。
- IMAGE: 使用的镜像。
- COMMAND: 启动容器时运行的命令。
- CREATED: 容器的创建时间。
- STATUS: 容器状态(状态有7种)。
  - created（已创建）
  - restarting（重启中）
  - running（运行中）
  - removing（迁移中）
  - paused（暂停）
  - exited（停止）
  - dead（死亡）
- PORTS: 容器的端口信息和使用的连接类型（tcp\udp）。
- NAMES: 自动分配的容器名称。

我们通过`docker logs` 命令，查看指定容器内的标准输出:

```bash
[root@pdai ~]# docker logs 1a51d2f023c9
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
hello world
```

最后我们看下，如何关闭后台实例

```bash
[root@pdai ~]# docker stop 1a51d2f023c9
1a51d2f023c9
[root@pdai ~]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
[root@pdai ~]#
```
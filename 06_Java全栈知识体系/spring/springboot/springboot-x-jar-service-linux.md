# SpringBoot应用部署 - 在linux环境将jar制作成service

> 前文我们将SpringBoot应用打包成jar，那么如何将jar封装成service呢？本文主要介绍将SpringBoot应用部署成linux的service。@pdai

## 概述

> 基本的`java -jar`运行方式，和这种运行方式的缺陷。

### Java -jar运行？

Linux 运行jar包基本命令：

```bash
# 当前ssh窗口被锁定，可按CTRL + C打断程序运行，或直接关闭窗口，程序退出
java -jar XXX.jar

# &代表在后台运行。当前ssh窗口不被锁定，但是当窗口关闭时，程序中止运行。
java -jar XXX.jar &
```

nohup命令， nohup 意思是不挂断运行命令,当账户退出或终端关闭时,程序仍然运行

```bash
# 当用 nohup 命令执行作业时，缺省情况下该作业的所有输出被重定向到nohup.out的文件中。
nohup java -jar XXX.jar &  

# 输出重定向到temp.txt文件
nohup java -jar XXX.jar >temp.txt &  

# 程序在后台运行，当ssh窗口关闭，程序正常运行，且不会输出文件
nohup java -jar xx.jar >/dev/null 2>&1 &
```

### 这种运行方式的缺陷

> 这种运行方式有何缺陷呢？

1. 不优雅
2. 无法向Linux服务一样简单易用，具备start,stop,restart等service操作方式。以及开机自启等。

## 在Linux环境封装service

> 加入我们编译出了一个tech_arch-0.0.1-RELEASE.jar，如何将它封装成service呢？

### 文件准备

```bash
[root@docker opt]# tree -a
.
└── tech_doc
    ├── bin
    │   ├── logs
    │   │   └── service.2018-10-31.log
    │   └── tech_arch-0.0.1-RELEASE.jar
    └── tech_doc
```

### 创建启动文件

tech_doc

```bash
[root@docker opt]# cat tech_doc/tech_doc
#!/bin/sh

#------------------------------------------------
# function: services start
# author: pdai
# home: /opt/tech_doc/bin
# log: /var/log/tech_doc/process
#------------------------------------------------

HOME=/opt/tech_doc/bin
LOGHOME=/var/log/tech_doc/process


function serviceLoad()
{
  b=''
  i=0
  while [ $i -le  100 ]
  do
      printf "$1:[%-50s]%d%%\r" $b $i
      sleep 0.3
      i=`expr 2 + $i`
      b=#$b
  done
  echo
}

function svcStart()
{
  echo "Starting $2 ..."
  cd $1
  PID=$(ps -ef | grep "$4" | grep -v grep | awk '{print $2}')
  if [ -z "$PID" ]; then
          nohup java -jar $3  > $5 2> $6 &
    serviceLoad $SERVICE_NAME
          echo "$2 started ..."
  else
          echo "$2 is already running ..."
  fi
}

function svcStop()
{
  PID=$(ps -ef | grep "$1" | grep -v grep | awk '{print $2}')
  if [ -z "$PID" ]; then
          echo "$2 already stopped ..."
  else
    kill $PID
        echo "$2 is stoping ..."
  fi
}

function do_start()
{
  for FILE in `ls $HOME | grep jar`
  do
    FILE_NAME=$FILE
    SERVICE_JAR_PACKAGE_PATH=$HOME/$FILE
    SERVICE_NAME=${FILE_NAME%-[0-9]*}
    SERVICE_LOG_PATH="$LOGHOME/$SERVICE_NAME.log"
    SERVICE_ERR_LOG_PATH="$LOGHOME/$SERVICE_NAME.err"

    svcStart $HOME $SERVICE_NAME $SERVICE_JAR_PACKAGE_PATH $FILE_NAME $SERVICE_LOG_PATH $SERVICE_ERR_LOG_PATH
  done
}

function do_stop()
{
    for FILE in `ls $HOME | grep jar`
  do
    FILE_NAME=$FILE
    SERVICE_NAME=${FILE_NAME%-[0-9]*}
    SERVICE_PID_PATH="/tmp/$SERVICE_NAME.pid"

    svcStop $FILE_NAME $SERVICE_NAME
    sleep 1
  done
}

function do_check()
{
    for FILE in `ls $HOME | grep jar`
  do
    FILE_NAME=$FILE
    SERVICE_NAME=${FILE_NAME%-[0-9]*}
    PID=$(ps -ef | grep $FILE_NAME | grep -v grep | awk '{print $2}')
  if [ -z "$PID" ]; then
          echo "$SERVICE_NAME $PID is not running ..."
  else
        echo "$SERVICE_NAME $PID is running ..."
  fi

    sleep 1
  done
}

case "$1" in
    start)

        do_start
        echo start successful

    ;;
    stop)

        do_stop
        echo stop successful

    ;;
    restart)

        do_stop
              sleep 2
        do_start
        echo restart successful

    ;;
    status)

        do_check

    ;;
    *)
    echo "Usage: {start|stop|restart|status}" >&2
    exit 3
    ;;
esac
exit 0
```

### 制作服务

在init.d下创建服务

```bash
[root@docker init.d]# tree -a
.
├── functions
├── netconsole
├── network
├── README
└── tech-doc
```

tech-doc内容如下:

```bash
[root@docker opt]# cd /etc/init.d
[root@docker init.d]# ls
functions  netconsole  network  README  tech-doc
[root@docker init.d]# tree -a
.
├── functions
├── netconsole
├── network
├── README
└── tech-doc

0 directories, 5 files
[root@docker init.d]# ^C
[root@docker init.d]# cat tech-doc
#!/bin/sh
#
# /etc/init.d/tech-doc
# chkconfig: 2345 60 20
# description: ms.
# processname: tech-doc

SCRIPT_HOME=/opt/tech_doc

case $1 in
    start)
        sh $SCRIPT_HOME/tech_doc start
    ;;
    stop)
        sh $SCRIPT_HOME/tech_doc stop
    ;;
    restart)
        sh $SCRIPT_HOME/tech_doc stop
        sh $SCRIPT_HOME/tech_doc start
    ;;
    status)
        sh $SCRIPT_HOME/tech_doc status
    ;;
    *)
    echo "Usage: {start|stop|restart|status}" >&2
    exit 3
    ;;
esac
exit 0
```

### 赋予权限

```bash
chmod 777 /etc/init.d/tech-doc
```

### 开机自启

```bash
chkconfig --list
chkconfig tech-doc on
```

### 查看端口

```bash
netstat -nltp
```

### 查看防火墙

```bash
systemctl status firewalld
```

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos
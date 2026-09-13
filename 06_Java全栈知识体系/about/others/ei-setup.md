# EI Config Tool 开发配置

> 本文主要包含EI Config Tool的代码说明和配置。

## 模块结构

EI Config Tool整体模块关系如下：

![](https://www.pdai.tech/images/eiconfig/ei-setup-2.png)

> 上述功能模块的一些说明

- **WEB部分**
  - **WEB 接口部分**：EI-Config-Web-Backend
    - 提供API接口
    - 提供保存，加载，到处xml文件等
  - **WEB UI部分**：EI-Config
    - UI操作呈现
- **后端部分**
  - C++后台服务

## 前端接口部分

> **技术栈**：Java + SpringBoot + Jackson

- 代码导入和说明

使用IDEA 工具来开发这个项目，IDEA可以从官方网站下载，目前来说主要的开发IDE工具是IEDA和Eclipse，前者更为好用。

![](https://www.pdai.tech/images/eiconfig/ei-setup-3.jpg)

加载完代码以后，初步理解项目结构和入口。

![](https://www.pdai.tech/images/eiconfig/ei-setup-1.png)

代码结构说明如下：

```bash
+ com.ama.ei // 机构.项目名
  + common   // 公共的模块
    + aop    // 统一的Spring切面
    + constant // 项目常量
    + response // 统一的接口返回
  + config  // 项目配置类
  + controller // worker类，api的入口，这些api提供给
  + entity    // 实体类，DO和VO
  + service   // 服务类，供controller调用
  + util      // utils
  + EIApplication.java // 程序的入口
+ resources
  + static    // 前端编译出的文件
  + application.properties // 配置文件
+ pom.xml     // Java依赖包
```

- 本地运行

代码配置好以后，就可以开始运行了，点击如下绿色运行箭头

![](https://www.pdai.tech/images/eiconfig/ei-setup-4.jpg)

启动成功如下

![](https://www.pdai.tech/images/eiconfig/ei-setup-5.jpg)

接下来打开浏览器http://localhost:9999/doc.html，这个是前端给后端提供的接口

![](https://www.pdai.tech/images/eiconfig/ei-setup-6.jpg)

## 前端UI部分

> **技术栈**: VueJs + Ant Design Pro Vue

- 代码导入

使用VsCode进行前端开发，导入项目，（需要对前端项目有一定的了解）

![](https://www.pdai.tech/images/eiconfig/ei-setup-10.jpg)

代码结构说明如下：

```bash
+ src
  + api     // 封装和前端交互的api
  + assets  // 图标
  + components // 自定义组件
  + config  // 一些配置
  + core    // 核心组件引入
  + data    // 静态数据，本地测试的时候可以用，目前没啥用
  + layouts // 视图布局
  + routes  // 前端路由
  + store   // 本地转态保存
  + utils   // utils
  + views   // 视图页面
  + app.vue // app页面入口
```

- 前端和后端接口配置

给开发环境使用是.env.devlopment文件。

```bash
NODE_ENV=development
VUE_APP_PREVIEW=true
VUE_APP_API_BASE_URL=http://localhost:9999/api
VUE_APP_DOC_URL=http://localhost:9999/doc.html
```

集成环境下：

```bash
NODE_ENV=production
VUE_APP_PREVIEW=false
VUE_APP_API_BASE_URL=/api
VUE_APP_DOC_URL=/doc.html
```

- 配置和启动

安装前端依赖

```bash
npm install
```

启动服务

![](https://www.pdai.tech/images/eiconfig/ei-setup-11.jpg)

服务启动后，通过如下端口可以进行访问：

```bash
 DONE  Compiled successfully in 12359ms                                                                                                                下午8:35:37


  App running at:
  - Local:   http://localhost:8080/ 
  - Network: http://192.168.3.93:8080/

  Note that the development build is not optimized.
  To create a production build, run npm run build.
```

打开http://localhost:8080/

![](https://www.pdai.tech/images/eiconfig/ei-setup-13.jpg)

- 前端编译

![](https://www.pdai.tech/images/eiconfig/ei-setup-12.jpg)

## 前后端服务整合

将前端编译出的doc拷贝至后端api服务的static文件夹

![](https://www.pdai.tech/images/eiconfig/ei-setup-7.jpg)

这时候，你可以通过刚才后端服务启动方式进行启动，并且访问http://localhost:9999

![](https://www.pdai.tech/images/eiconfig/ei-setup-9.jpg)

整合之后，就是编译打包了：

![](https://www.pdai.tech/images/eiconfig/ei-setup-8.jpg)

这个jar包便是我们最后部署中所使用的jar包，jar包的部署可以参考部署文档。
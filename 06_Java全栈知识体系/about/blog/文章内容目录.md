# 文章内容目录

# 第一部分 - 博客/文档系统的搭建

> 搭建博客有很多选择，平台性的比如: 知名的CSDN, 博客园, 知乎，简书等；自己搭建比如 Hexo, Gitbook, Docisify等等。我有一颗不安分的心，每种我都用过...但是最后的最后我还是选择了将博客逐移至自己搭建的vuepress。 @pdai

## 博客/文档搭建前言

### 有哪些选择

搭建博客有很多选择，平台性的比如: 知名的CSDN, 博客园, 知乎，简书等；自己搭建比如 Hexo, Gitbook, Docisify等等。

### 我做了哪些尝试

- 自己写：我用java手写了一个系统
- Docisify等工具
- 博客园等平台

#### 自己写：我用java手写了一个系统

> 以下系统由我独立设计，开发和运维(总计四万多行代码吧), 这里只展示博客文档部分。以下图片是我在之前博客园写文章截图的：

- markdown编辑

![](https://www.pdai.tech/images/blog/blog-choose-1.png)

- 文章清单

![](https://www.pdai.tech/images/blog/blog-choose-2.png)

- 支持导出各种形式

![](https://www.pdai.tech/images/blog/blog-choose-3.png)

- 支持共享给其它虚拟组织

![](https://www.pdai.tech/images/blog/blog-choose-4.png)

等等。

#### Docisify等工具

> 之前用搭建过基于K8S的完整的平台，写了系列的文章总结。用的工具就是用的[Docisify](https://docsify.js.org)。

效果如下：

![](https://www.pdai.tech/images/blog/blog-choose-5.png)

#### 博客园等平台

支持自定义样式，自定义js权限，这表明自由控制程度会很高(这点看CSDN就略保守了)；但是网站长期没有更新，主页样式感觉停留在十年前；客户端程序，略有点low;

效果如下：

![](https://www.pdai.tech/images/blog/blog-choose-6.png)

具体可以看我写的这篇：[【博客园配置】博客园自定义配置有哪些骚操作](https://www.cnblogs.com/pengdai/p/9168079.html)

### 为什么现在用vuepress

类似博客/文档工具比对vuepress可以看出其优势：以下内容摘自: [Vuepress官网](https://vuepress.vuejs.org)

- Nuxt

VuePress 能做的事情，Nuxt 理论上确实能够胜任，但 Nuxt 是为构建应用程序而生的，而 VuePress 则专注在以内容为中心的静态网站上，同时提供了一些为技术文档定制的开箱即用的特性。

- Docsify / Docute

这两个项目同样都是基于 Vue，然而它们都是完全的运行时驱动，因此对 SEO 不够友好。如果你并不关注 SEO，同时也不想安装大量依赖，它们仍然是非常好的选择！

- Hexo

Hexo 一直驱动着 Vue 的文档 —— 事实上，在把我们的主站从 Hexo 迁移到 VuePress 之前，我们可能还有很长的路要走。Hexo 最大的问题在于他的主题系统太过于静态以及过度地依赖纯字符串，而我们十分希望能够好好地利用 Vue 来处理我们的布局和交互，同时，Hexo 的 Markdown 渲染的配置也不是最灵活的。

- GitBook

我们的子项目文档一直都在使用 GitBook。GitBook 最大的问题在于当文件很多时，每次编辑后的重新加载时间长得令人无法忍受。它的默认主题导航结构也比较有限制性，并且，主题系统也不是 Vue 驱动的。GitBook 背后的团队如今也更专注于将其打造为一个商业产品而不是开源工具。

## 博客/文档工具vuepress介绍

VuePress 由两部分组成：第一部分是一个[极简静态网站生成器](https://github.com/vuejs/vuepress/tree/master/packages/%40vuepress/core)，它包含由 Vue 驱动的`主题系统`和`插件 API`，另一个部分是为书写技术文档而优化的`默认主题`，它的诞生初衷是为了支持 Vue 及其子项目的文档需求。

每一个由 VuePress 生成的页面都带有预渲染好的 HTML，也因此具有非常好的加载性能和搜索引擎优化(SEO)。同时，一旦页面被加载，Vue 将接管这些静态内容，并将其转换成一个完整的单页应用(SPA)，其他的页面则会只在用户浏览到的时候才按需加载。

### vuepress是如何工作的?

事实上，一个 VuePress 网站是一个由 [Vue](http://vuejs.org/)、[Vue Router](https://github.com/vuejs/vue-router) 和 [webpack](http://webpack.js.org/) 驱动的单页应用。如果你以前使用过 Vue 的话，当你在开发一个自定义主题的时候，你会感受到非常熟悉的开发体验，你甚至可以使用 Vue DevTools 去调试你的自定义主题。

在构建时，我们会为应用创建一个服务端渲染(SSR)的版本，然后通过虚拟访问每一条路径来渲染对应的HTML。这种做法的灵感来源于 [Nuxt](https://nuxtjs.org/) 的 `nuxt generate` 命令，以及其他的一些项目，比如 [Gatsby](https://www.gatsbyjs.org/)。

### vuepress 一些特性

- 为技术文档而优化的内置Markdown拓展
- 在Markdown文件中使用Vue组件的能力
- Vue驱动的自定义主题系统
- 自动生成Service Worker(支持PWA)
- Google Analytics集成
- 基于Git的"最后更新时间"
- 多语言支持
- 响应式布局
- 天然的SEO能力，对比Docsify这种前端渲染HTML要好很多

### vuepress 插件架构

其整体的插件架构案例: [Vuepress 插件架构案例](https://vuepress.vuejs.org/zh/plugin/)

![](https://www.pdai.tech/images/blog/blog-architecture.png)

## 博客/文档基础搭建

> 文档的搭建比较简单，主要记录流程，有些步骤你在阅读的时候如果觉得不需要, 可以直接略过。

### brew安装或者更新

先卸载已安装的homebrew，命令如下：

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"
```

然后重新安装：

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

通过该方法直接获取最新的homebrew，出现预期效果。注：上述可以修复`chown: /usr/local: Operation not permitted`这个问题。

如果觉得慢，需要更换 Brew 镜像源, 请看考: [更换 Brew 镜像源](https://blog.csdn.net/zhxuan30/article/details/81517446)

### 更新node和npm

> Vuepress对Node版本要求： Node.js 版本 >= 8.6。

- 方法1: 手动删除/usr/local/bin 下面的node和npm文件
- 方法2: 覆盖现有版本brew link --overwrite node

如有需要，请参考这两篇文章：

- [mac 用brew升级node最新版本，npm出现问题问题解决](https://blog.csdn.net/bz151531223/article/details/80081565)
- [brew 升级 node版本](https://www.jianshu.com/p/39ef3b51ca6f)

### 配置vuepress工作目录

- 全局安装vuepress

```bash
yarn global add vuepress
```

- 创建项目并初始化目录结构

```bash
# 目录
mkdir tech-arch-doc
cd tech-arch-doc
# 初始化
yarn init -y # 或者 npm init -y
# 放markdown的文件夹
mkdir md
# package.json, 里面放的内容看后文
touch package.json
# 放vuepress相关
mkdir .vuepress
cd .vuepress
# 创建config.js, 里面放的内容看后文
touch config.js
# 放图片和CNAME
mkdir public
# 放样式的
mkdir styles
# 在里面创建放图片
cd public
mkdir _images
```

最后的结构大概是这样：(其它灰色的文件夹是编译出来的)

![](https://www.pdai.tech/images/blog/blog-struct-1.png)

### 添加配置和内容

- 添加主页面

```java
---
home: true
heroImage: /images/index-read.gif
actionText: 快速开始 →
actionLink: /md/java/basic/java-basic-oop.md
features:
- title: 夯实基础
  details: 不积跬步无以至千里, 仰望星空还需脚踏实地
- title: 构建体系
  details: 告别碎片化学习，帮助你构筑你自己的知识体系
- title: 全栈开发
  details: 以Java开发为背景，全栈开发，DevOps
footer: © 2017-present pdai
---
```

- config.js配置

```javascript
module.exports = {
    port: "3000",
    dest: "docs",
    ga: "UA-xxxxx-1",
    base: "/",
    markdown: {
        lineNumbers: true,
        externalLinks: {
            target: '_blank', rel: 'noopener noreferrer'
        }
    },
    locales: {
        "/": {
            lang: "zh-CN",
            title: "Java 全栈知识体系",            
            description: "包含: Java 基础, Java 部分源码, JVM, Spring, Spring Boot, Spring Cloud, 数据库原理, MySQL, ElasticSearch, MongoDB, Docker, k8s, CI&CD, Linux, DevOps, 分布式, 中间件, 开发工具, Git, IDE, 源码阅读，读书笔记, 开源项目..."
        }
    },
    head: [
        // ico
        ["link", {rel: "icon", href: `/favicon.ico`}],
        // meta
        ["meta", {name: "robots", content: "all"}],
        ["meta", {name: "author", content: "pdai"}],
        ["meta", {name: "keywords", content: "Java 全栈知识体系, java体系, java知识体系, java框架,java详解,java学习路线,java spring, java面试, 知识体系, java技术体系, java编程, java编程指南,java开发体系, java开发,java教程,java,java数据结构, 算法, 开发基础"}],
        ["meta", {name: "apple-mobile-web-app-capable", content: "yes"}]
    ],
    plugins: [
    ],
    themeConfig: {
        // repo: "realpdai/tech-arch-doc",
        docsRepo: "realpdai/tech-arch-doc",
        // logo: "/logo.png",
        editLinks: true,
        sidebarDepth:0,
        locales: {
            "/": {
                label: "简体中文",
                selectText: "Languages",
                editLinkText: "在 GitHub 上编辑此页",
                lastUpdated: "上次更新",
                nav: [
                ],
                sidebar: {
                }
            }
        }
    }
};
```

- package.json配置

进入项目目录

```json
{
  "name": "tech-arch-doc",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "vuepress dev",
    "build": "vuepress build"
  },
  "devDependencies": {
    "vuepress": "^1.0.2"
  }
}
```

- 本地测试

```bash
vuepress dev
```

初步效果：

![](https://www.pdai.tech/images/blog/blog-try-1.png)

- 要生成静态的 HTML 文件，运行:

> 默认情况下，文件将会被生成在 .vuepress/dist，当然，你也可以通过 .vuepress/config.js 中的 dest 字段来修改，生成的文件可以部署到任意的静态文件服务器上

请参考官网 https://vuepress.vuejs.org/zh/guide/getting-started.html#%E5%85%A8%E5%B1%80%E5%AE%89%E8%A3%85

```bash
vuepress build
```

## 文档搭建插件和配置

> 这里主要介绍文档搭建除了默认加载的配置和插件之外，新增加的插件和配置。

### 添加文档附加样式配置: 主题

> 注意很多网上的例子还是基于老的版本的，甚至我用vuepress的时候，官网还没有更新过来。

最佳配置请参考: [这里](https://vuepress.vuejs.org/zh/miscellaneous/design-concepts.html#overriding): (其它官网的配置都没有更新)

- index.styl - 覆盖的样式

```stylus
.custom-page-class{
    /* 自定义的样式 */
}

// markdown blockquote
blockquote
  font-size 1rem
  color #2c3e50;
  border-left .5rem solid #42b983
  background-color #f3f5f7
  margin 1rem 0
  padding 1rem 0 1rem 1rem

  & > p
    margin 0

// markdown h2
h2
  font-size 1.65rem
  padding-bottom 1rem
  border-bottom 1px solid $borderColor
```

- palette.styl - 样式配置覆盖

```stylus
// 内容的宽度
$contentWidth = 100%

// 颜色
$accentColor = #3eaf7c
$textColor = #2c3e50
$borderColor = #eaecef
$codeBgColor = #282c34
```

### 添加返回最上插件

> 文章很长，添加右下角一键返回顶部按钮，官网提供了 back-to-top 插件.

安装

```javascript
yarn add -D @vuepress/plugin-back-to-top@next
# OR npm install -D @vuepress/plugin-back-to-top@next
```

使用

```javascript
module.exports = {
  plugins: ['@vuepress/back-to-top']
}
```

插件使用你还可以参考：[插件官网](https://vuepress.vuejs.org/zh/plugin/official/plugin-back-to-top.html#%E5%AE%89%E8%A3%85)

### 添加图片缩放插件

> 图片缩放可以使用@vuepress/plugin-medium-zoom插件，它基于medium-zoom 插件。

```bash
yarn add -D @vuepress/plugin-medium-zoom@next
# OR npm install -D @vuepress/plugin-medium-zoom@next
```

简单使用:

```javascript
module.exports = {
  plugins: ['@vuepress/medium-zoom']
}
```

自定义选项:

```javascript
module.exports = {
  plugins: {
    '@vuepress/medium-zoom': {
      selector: 'img.zoom-custom-imgs',
      // medium-zoom options here
      // See: https://github.com/francoischalifour/medium-zoom#options
      options: {
        margin: 16
      }
    }
  }
}
```

效果可以点击本文中的图片查看, 具体使用你可以参考: [插件官网](https://vuepress.vuejs.org/zh/plugin/official/plugin-medium-zoom.html)。

### 添加评论插件

> 代码托管平台遵从 [OAuth 2 spec](https://tools.ietf.org/html/rfc6749) 提供了 OAuth API。Vssue 利用平台提供的 OAuth API，使得用户可以登录并发表评论。那么有哪些评论插件可以使用? 这里使用Vssue，它比较新，可能知道的人还不多。@pdai

**Vssue** , [**Gitalk**](https://github.com/gitalk/gitalk) 和 [**Gitment**](https://github.com/imsun/gitment)，为何选择Vssue：

- **Vssue** 支持 Github、Gitlab 和 Bitbucket，并且很容易扩展到其它平台。**Gitment** 和 **Gitalk** 仅支持 Github。
- **Vssue** 可以发表、编辑、删除评论。**Gitment** 和 **Gitalk** 仅能发表评论。
- **Vssue** 是基于 [Vue.js](https://vuejs.org) 开发的，可以集成到 Vue 项目中，并且提供了一个 VuePress 插件。 **Gitment** 基于原生JS，而 **Gitalk** 基于 [Preact](https://github.com/developit/preact)。

下面是 Vssue 的简要工作过程：

![](https://www.pdai.tech/images/blog/how-vssue-works-zh.png)

用户在平台的授权页面允许 Vssue 接入后，平台会带有 `code` 或 `token` 重定向回 Vssue 的页面(如果是 `code` ，Vssue 则会根据 `code` 向平台请求 `token`)。

Vssue 获取 `token` 后，会将 `token` 存储在 localstorage 中，于是用户就成功使用平台的帐号“登录”到了 Vssue。

接下来， Vssue 就可以获取用户的基本信息、获取当前页面的评论，用户也可以发表评论了。

添加如下配置：具体参考[Vssue 官网教程](https://vssue.js.org/zh/guide/vuepress.html)

```javascript
plugins: {
  '@vssue/vuepress-plugin-vssue': {
    // 设置 `platform` 而不是 `api`
    platform: 'github',

    // 其他的 Vssue 配置
    owner: 'OWNER_OF_REPO',
    repo: 'NAME_OF_REPO',
    clientId: 'YOUR_CLIENT_ID',
    clientSecret: 'YOUR_CLIENT_SECRET',
  },
},
```

效果如下：

![](https://www.pdai.tech/images/blog/blog-comments-1.png)

### 添加Vuepress文档的导出

注意：

导出页面只在我本地开放，线上功能我暂时关闭了。

自己写了文档PDF的导出功能(Page, Group, Current是我导出功能里的`代号`): Page = Group1+...GroupN, Group = Current1+...CurrentN

- 当前页面导出
- Group页面导出：主要用来导出一组或者多组章节下面的所有文章。
- Page页面导出

以SpringBoot部分章节导出为例，导出效果如下：

![](https://www.pdai.tech/images/blog/blog-ssl-export-1.png)

### 添加svg label标签

你是不是常看到别人的项目中加了![](https://img.shields.io/badge/pdai-full stack-blue)这种标签? 这种标签主要基于svg，主要有两种:

- 比如Travis CI 提供的: [本网站Build结果](https://travis-ci.com/realpdai/tech-arch-doc.svg?branch=master)
- 这个网站还可以定制：[定制icon svg](https://shields.io/)

添加后效果(状态为自动获取)：

[![](https://travis-ci.com/realpdai/tech-arch-doc.svg?branch=master)](https://travis-ci.com/realpdai/tech-arch-doc.svg?branch=master)[![](https://img.shields.io/github/license/realpdai/tech-arch-doc)](https://github.com/realpdai/tech-arch-doc/blob/master/LICENSE)![](https://img.shields.io/badge/pdai-full stack-blue)

### 添加百度统计

- 百度统计主要辅助我分析页面访问量，直接去: [百度统计官网](https://tongji.baidu.com)

> 注意百度统计添加, 考虑在每个页面点击时作记录，在enhanceApp.js中拦截router:

```javascript
export default ({router}) => {
    router.beforeEach((to, from, next) => {
        // @pdai: 对每个页面点击添加百度统计
        if(typeof _hmt!='undefined'){
            if (to.path) {
                _hmt.push(['_trackPageview', to.fullPath]);
            }
        }
        
        // continue
        next();       
    })
};
```

百度统计里某个页面效果如下：

![](https://www.pdai.tech/images/blog/blog-ssl-tongji-1.png)

### 添加Copy自动加版权信息

> 复制你网站时，禁用复制或者添加版权信息等。

安装

```bash
npm install vuepress-plugin-copyright
```

配置

```javascript
// .vuepress/config.js
module.exports = {
  plugins: [
    [
      'copyright',
      {
        noCopy: true, // 选中的文字将无法被复制
        minLength: 100, // 如果长度超过 100 个字符
      },
    ],
  ],
}
```

效果, 拷贝本页面会自动添加：

```html
著作权归 xxxx 所有。
链接：/md/about/blog/blog-build-vuepress.html
```

更多请参考插件：[vuepress-plugin-sitemap](https://vuepress.github.io/en/plugins/copyright/#installation)

### 添加SEO优化

> 这里给个链接供参考，我这边自己添加的meta信息没有用它。

- [vuepress-plugin-autometa](https://github.com/webmasterish/vuepress-plugin-autometa)

### 添加百度站点自动推送

> 主要用于向百度站点自动推送，有助于SEO。

安装

```bash
npm install -D vuepress-plugin-baidu-autopush
```

添加配置

```javascript
module.exports = {
  plugins: [
    'vuepress-plugin-baidu-autopush'
  ]
};
```

更多请参考插件：[vuepress-plugin-baidu-autopush](https://github.com/IOriens/vuepress-plugin-baidu-autopush)

### 添加Sitemap信息

> 主要用于生成站点的Sitemap，有助于SEO。

安装

```bash
npm install vuepress-plugin-sitemap
```

配置

```javascript
// .vuepress/config.js
module.exports = {
  plugins: {
    'sitemap': {
      hostname: ''
    },
  }
}
```

更多请参考插件：[vuepress-plugin-sitemap](https://github.com/ekoeryanto/vuepress-plugin-sitemap)

### 添加代码拷贝

> 在代码区，添加一个拷贝按钮，用来拷贝代码。

安装

```bash
npm install vuepress-plugin-code-copy
```

配置

```javascript
module.exports = {
    plugins: [['vuepress-plugin-code-copy', true]]
}
```

更多请参考插件：[vuepress-plugin-code-copy](https://github.com/znicholasbrown/vuepress-plugin-code-copy)

### 更多插件配置

请参考 [awesome-vuepress](https://github.com/vuepressjs/awesome-vuepress)

## 博客/文档稍完整配置清单

- config.js部分内容

```javascript
module.exports = {
    port: "3000",
    dest: "docs",
    ga: "UA-xxxxxxxxxxx-1",
    base: "/",
    markdown: {
        lineNumbers: true,
        externalLinks: {
            target: '_blank', rel: 'noopener noreferrer'
        }
    },
    locales: {
        "/": {
            lang: "zh-CN",
            title: "Java 全栈知识体系",            
            description: "包含: Java 基础, Java 部分源码, JVM, Spring, Spring Boot, Spring Cloud, 数据库原理, MySQL, ElasticSearch, MongoDB, Docker, k8s, CI&CD, Linux, DevOps, 分布式, 中间件, 开发工具, Git, IDE, 源码阅读，读书笔记, 开源项目..."
        }
    },
    head: [
        // ico
        ["link", {rel: "icon", href: `/favicon.ico`}],
        // meta
        ["meta", {name: "robots", content: "all"}],
        ["meta", {name: "author", content: "pdai"}],
        ["meta", {name: "keywords", content: "Java 全栈知识体系, java体系, java知识体系, java框架,java详解,java学习路线,java spring, java面试, 知识体系, java技术体系, java编程, java编程指南,java开发体系, java开发,java教程,java,java数据结构, 算法, 开发基础"}],
        ["meta", {name: "apple-mobile-web-app-capable", content: "yes"}],
        // baidu statstic
        ["script", {src: "https://hm.baidu.com/hm.js?xxxxxxxxxxx"}]
    ],
    plugins: [
        ['@vuepress/back-to-top', true],
        ['@vuepress/medium-zoom', {
            selector: 'img',
            // See: https://github.com/francoischalifour/medium-zoom#options
            options: {
              margin: 16
            }
        }],
        // see: https://vssue.js.org/guide/vuepress.html#usage
        ['@vssue/vuepress-plugin-vssue', {
            // set `platform` rather than `api`
            platform: 'github',
            // all other options of Vssue are allowed
            owner: 'realpdai',
            repo: 'tech-arch-doc-comments',
            clientId: 'xxxxxxxxxxx',
            clientSecret: 'xxxxxxxxxxxxxxxxxxxxxx',
        }],
        // see: https://vuepress.github.io/zh/plugins/copyright/#%E5%AE%89%E8%A3%85
        ['copyright', {
            noCopy: false, // 允许复制内容
            minLength: 100, // 如果长度超过 100 个字符
            authorName: "",
            // clipboardComponent: "请注明文章出处, [Java 全栈知识体系]()"
        }],
        // see: https://github.com/ekoeryanto/vuepress-plugin-sitemap
        ['sitemap', {
            hostname: ''
        }],
        // see: https://github.com/IOriens/vuepress-plugin-baidu-autopush
        ['vuepress-plugin-baidu-autopush', {
            
        }],
        // see: https://github.com/znicholasbrown/vuepress-plugin-code-copy
        [['vuepress-plugin-code-copy', true]]
        // ...
    ],
    themeConfig: {
        //repo: "realpdai/tech-arch-doc",
        docsRepo: "realpdai/tech-arch-doc",
        //logo: "/logo.png",
        editLinks: true,
        sidebarDepth:0,
        locales: {
            "/": {
                label: "简体中文",
                selectText: "Languages",
                editLinkText: "在 GitHub 上编辑此页",
                lastUpdated: "上次更新",
                nav: [
                    {
                        text: '关于', link: '/md/about/me/about-me.md'
                    }
                ],
                sidebar: {
                    "/md/about/": genSidebar4About()
                }
            }
        }
    }
};

// About page
function genSidebar4About(){
    return [
        {
            title: "关于",
            collapsable: false,
            sidebarDepth: 0, 
            children: [
                "me/about-me.md",
                "me/about-content.md",
                "me/about-content-style.md",
                "me/about-arch.md",
                "me/about-motivation.md"
            ]
        },
        {
            title: "关于 - 本文档的搭建",
            collapsable: false,
            sidebarDepth: 0, 
            children: [
                "blog/blog-build-vuepress.md", 
                "blog/blog-build-ci.md",
                "blog/blog-build-cd.md",
                "blog/blog-build-ssl.md"
            ]
        }
    ];
}
```

- package.json

```json
{
  "name": "tech-arch-doc",
  "version": "2.0.1",
  "private": true,
  "scripts": {
    "dev": "vuepress dev",
    "build": "vuepress build"
  },
  "devDependencies": {
    "@vuepress/plugin-back-to-top": "^1.0.3",
    "@vuepress/plugin-medium-zoom": "^1.0.4",
    "vuepress": "^1.0.2"
  },
  "dependencies": {
    "@vssue/api-github-v3": "^1.1.2",
    "@vssue/vuepress-plugin-vssue": "^1.2.0",
    "vuepress-plugin-baidu-autopush": "^1.0.1",
    "vuepress-plugin-code-copy": "^1.0.4-alpha",
    "vuepress-plugin-copyright": "^1.0.2",
    "vuepress-plugin-sitemap": "^2.3.0"
  }
}
```

- enhanceApp.js

```javascript
export default ({router}) => {
    router.beforeEach((to, from, next) => {
        // @pdai: 对每个页面点击添加百度统计
        if(typeof _hmt!='undefined'){
            if (to.path) {
                _hmt.push(['_trackPageview', to.fullPath]);
            }
        }
        
        // continue
        next();     
    })
};
```

- index.styl

```stylus
.custom-page-class{
    /* 自定义的样式 */
}

// markdown blockquote
blockquote
  font-size 1rem
  color #2c3e50;
  border-left .5rem solid #42b983
  background-color #f3f5f7
  margin 1rem 0
  padding 1rem 0 1rem 1rem

  & > p
    margin 0

// markdown h1
h1
  font-size 2rem
  padding-bottom 1rem
  border-bottom 1px solid $borderColor

// markdown h2
h2
  font-size 1.65rem
  border-bottom 0px solid $borderColor

// custom block for tip
.custom-block
  .custom-block-title
    font-weight 600
    margin-bottom -0.4rem
  &.tip, &.warning, &.danger
    padding .1rem 1.5rem
    border-left-width .5rem
    border-left-style solid
    margin 1rem 0
  &.tip
    background-color #dfefff
    border-color #428eb9

// logo
.navbar
  .logo
    height $navbarHeight - 1.6rem
    min-width $navbarHeight - 1.6rem
    margin-right 0rem
    vertical-align top
```

- palette.styl

```stylus
// 内容的宽度
$contentWidth = 100%

// 颜色
$accentColor = #3eaf7c
$textColor = #2c3e50
$borderColor = #eaecef
$codeBgColor = #282c34
```

## vuepress 其它参考资源

- [VuePress 官网](https://vuepress.vuejs.org/zh/)
- [VuePress Github](https://github.com/vuejs/vuepress)
- [VuePress 社区](https://vuepress.github.io) VuePress社区维护的生态系统
- [awesome-vuepress](https://github.com/vuepressjs/awesome-vuepress) // 注意：vuepress插件分官方(包括官方社区)和社区两个维护，在里面都可以找到

# 第二部分 - 博客/文档的自动编译

> 文档托管在Github，有几种选择: Github自带的Github Actions，或者插件Travis CI， 或者插件Circle CI。@pdai

## Travis CI

> 注意: Travis CI有个坑爹的地方要注意: 它有travis.com和travis.org两个网站，一个是对公有项目，一个是对私有项目；然后，github是可以在公有和私有项目中切换的，于是在切换后，一些配置可能无法正确设置。

### Github 启用插件

进入 https://github.com/marketplace/travis-ci

![](https://www.pdai.tech/images/blog/blog-ci-1.png)

### 配置插件

![](https://www.pdai.tech/images/blog/blog-ci-2.png)

### 添加.travis.yml

> 注意: 这里只是简单做编译操作，您可以将编译的结果(静态的html文件)强制推送至当前仓库专门放编译后文件的分支；也可以在自己的服务器上安装travis-cli，在travis.com(注意不是travis.org)生成证书信息(自动生成相关环境变量)，来进行自动化部署。

这里上述两种方案都没有采用，是因为:

- 1)travis-cli对私有项目自动添加证书信息支持不够；
- 2)同时本文档中静态资源较多，拉取编译结果较大；
- 3)github 拉较大资源速度稳定性无法保障，原因你懂的；相对来说用webhook方式已经够了。

```json
language: node_js

sudo: false

node_js:
  - "12"

cache:
  yarn: true
  directories:
    - node_modules

branches:
  only:
    - master

env:
  global:
    - GITHUB_REPO: github.com/realpdai/tech-arch-doc.git

before_install:
  - export TZ=Asia/Shanghai

script:
  - vuepress build
```

### 触发编译

![](https://www.pdai.tech/images/blog/blog-ci-4.png)

### 查看最后提交编译状况

![](https://www.pdai.tech/images/blog/blog-ci-5.png)

![](https://www.pdai.tech/images/blog/blog-ci-6.png)

### 生成build 状态svg

![](https://www.pdai.tech/images/blog/blog-ci-3.png)

# 第三部分 - 博客/文档的自动部署

> 本文主要介绍 当前文档是如何在我自己的服务器自动编译部署的。@pdai

## 文档编译和部署流程

![](https://www.pdai.tech/images/blog/blog-ssl-cd-1.png)

## 搭建

> 之前购买了一个低配的阿里云虚拟机，系统是CentOS 7.x。

### 安装NodeJS

- 添加yum源

```bash
curl -sL https://rpm.nodesource.com/setup_10.x | bash -
```

- yum install

```bash
yum install -y nodejs
```

其它方式可以参考此文 https://blog.csdn.net/bbwangj/article/details/82253785

### 清理原有部分服务

> 之前服务器上搭建过gitlab-ee，jenkins，httpd等，由于我自己的代码托管已经切换至github的私有仓库，所以现在需要清理下；不需要清理的，请略过。

- 清理gitlab-ee

https://blog.csdn.net/huhuhuemail/article/details/80519433

- 清理httpd

https://www.cnblogs.com/richardcastle/p/8296166.html

### 安装Nginx和配置

- 安装

https://www.centos.bz/2018/01/centos-7%EF%BC%8C%E4%BD%BF%E7%94%A8yum%E5%AE%89%E8%A3%85nginx/

- 配置开机自启 https://www.cnblogs.com/jepson6669/p/9131217.html
- 配置nginx.conf

https://www.cnblogs.com/alvin-niu/p/9502286.html

- 配置firewalld

https://blog.csdn.net/benchem/article/details/79605598

### 部署项目

通过webhook触发编译并reload nginx

# 第四部分 - 博客/文档的域名，HTTPS，备案

> 本文主要记录 本文档的域名，HTTPS，备案。 @pdai

文档的域名，HTTPS，备案 这三个步骤不能反，因为存在依赖关系。

## 申请域名

- 申请: 万网

![](https://www.pdai.tech/images/blog/blog-ssl-ali-8.png)

- 申请域名

![](https://www.pdai.tech/images/blog/blog-ssl-ali-9.png)

## https

- 阿里云上: SSL证书

![](https://www.pdai.tech/images/blog/blog-ssl-ali-0.png)

- 申请证书

![](https://www.pdai.tech/images/blog/blog-ssl-ali-1.png)

- 证书审核

> 30分钟之内就审核完成

![](https://www.pdai.tech/images/blog/blog-ssl-ali-2.png)

- 证书详情

> 这个详情页面在备案的时候需要拍照上传。

![](https://www.pdai.tech/images/blog/blog-ssl-ali-7.png)

- 证书下载

![](https://www.pdai.tech/images/blog/blog-ssl-ali-6.png)

## 备案

> 80/443端口通过域名直接访问是需要备案的，在18年的时候我搭建过的个人网站是不要备案的。

- 备案前访问 pdai.tech

![](https://www.pdai.tech/images/blog/blog-ssl-ali-3.png)

- 进入备案

![](https://www.pdai.tech/images/blog/blog-ssl-ali-4.png)

> 期间需要手机通过阿里云人脸认证，并上传 身份证，域名和证书拍照等。

- 备案审核

![](https://www.pdai.tech/images/blog/blog-ssl-ali-5.png)

> 注意备案初审由阿里云代理的，要求: 个人网站必须命名为`xxxx的个人博客`或者`xxx的个人主页`，否则备案不通过。申请的周期大概最多是20天，申请完了之后工信部会发短信到登记到手机号，之后到8小时就可以使用了。

## 服务器资源选择

> 那么搭建这样的网站需要多少服务器资源呢，阿里云坑的地方是新用户首年都便宜，后面续费就贵了。

- 看下搭建需要多少资源

![](https://www.pdai.tech/images/blog/blog-ssl-ali-10.png)

- 看下费用

> 推荐选择1CPU，1-2G内存即可；1Core-1GB一年价格287多，选择五年也就642多；后期如有需求，可以在线`增加配置`

![](https://www.pdai.tech/images/blog/blog-ssl-ali-11.png)

- 关于续费，我之前选择是2CPU，4GB内存；当初一年是780，续费价格是2363；

![](https://www.pdai.tech/images/blog/blog-ssl-ali-12.png)

提示

后续: 我将阿里到服务器降级到了1U 1GB，但是使用Vuepress build 编译静态页面时内存需要700MB，这将导致内存不够。我这边考虑使用swap方式，置换一些内存资源放置swap磁盘。

- Swap空间

参考文章如下: https://blog.csdn.net/u010457406/article/details/83753384

编译前

![](https://www.pdai.tech/images/blog/about-ssl-swap-1.png)

编译中 (内存不够会置换至swap区)

![](https://www.pdai.tech/images/blog/about-ssl-swap-2.png)

# 最终的效果

![](https://www.pdai.tech/images/blog/final.png)
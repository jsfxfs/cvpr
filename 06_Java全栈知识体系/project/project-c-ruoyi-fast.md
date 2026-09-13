# 白银 - 项目之单包应用全模块

> 不要看此项目使用了SpringBoot2, 我依然把它的技术栈归为10年前的技术栈，因为作者在写这个项目的时候依然是借鉴的老项目的技术思想；为什么还是拿这个项目作为展示呢？
>
> 1. 经典的技术栈 - SpringMVC + MyBatis
> 2. 经典的功能设计 - OA或者CRM功能设计
> 3. 基于此的项目演进，可以帮助你理解后续这种项目开发是如何横向和纵向演进的。 可以很肯定的说，我们不再会写出这样“冗余”的代码

- 单机后端应用模块演化
  - User 增删查改
  - 增加Shiro登录模块
  - RBAC - 增加Role模块
  - RBAC - 增加Menu模块
  - RBAC - 增加Shiro授权模块
  - 数据域控制 - 增加Dept模块
  - 数据域控制 - 增加POST模块
  - 公共 - 增加Dict模块
  - 公共 - 增加Notice模块
  - 公共Monitor - 增加Log模块
  - 公共Monitor - 增加Metrics模块
  - 公共Monitor - 增加DB Monitor模块
  - 公共内容 - Util，常量，异常等
  - 用户状态持久化
  - 数据域控制
  - ORM重复化 - MyBatis Code Generator
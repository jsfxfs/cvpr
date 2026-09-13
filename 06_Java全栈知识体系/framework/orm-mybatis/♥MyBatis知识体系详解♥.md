# ♥MyBatis知识体系详解♥

> MyBatis知识体系详解。@pdai

## 架构图

![](https://www.pdai.tech/images/mybatis/mybatis-y-arch-1.png)

## 相关文章

- [MyBatis详解 - 总体框架设计](MyBatis详解 - 总体框架设计.md)
  - MyBatis整体架构包含哪些层呢？这些层次是如何设计的呢？
- [MyBatis详解 - 初始化基本过程](MyBatis详解 - 初始化基本过程.md)
  - 从上文我们知道MyBatis和数据库的交互有两种方式有Java API和Mapper接口两种，所以MyBatis的初始化必然也有两种；那么MyBatis是如何初始化的呢？
- [MyBatis详解 - 配置解析过程](MyBatis详解 - 配置解析过程.md)
  - 【本文为中优先级】通过上文我们知道MyBatis初始化过程中会解析配置，那具体是如何解析的呢？
- [MyBatis详解 - 官网配置清单](MyBatis详解 - 官网配置清单.md)
  - 【本文为低优先级】通过上文我们知道配置是如何加载并初始化的，那MyBatis提供了哪些配置呢？通过MyBatis官网文档我们一探究竟。PS：对于清单型的，只需要大致浏览且在使用时能快速查找即可，所以是低优先级的。
- [MyBatis详解 - Mapper映射文件配置](MyBatis详解 - Mapper映射文件配置.md)
  - 在mapper文件中，以mapper作为根节点，其下面可以配置的元素节点有： select, insert, update, delete, cache, cache-ref, resultMap, sql; 本文将Mapper映射文件配置进行详解。
- [MyBatis详解 - sqlSession执行流程](MyBatis详解 - sqlSession执行流程.md)
  - 前面的章节主要讲mybatis如何解析配置文件，这些都是一次性的过程。从本章开始讲解动态的过程，它们跟应用程序对mybatis的调用密切相关。
- [MyBatis详解 - 动态SQL使用与原理](MyBatis详解 - 动态SQL使用与原理.md)
  - 动态 SQL 是 MyBatis 的强大特性之一。如果你使用过 JDBC 或其它类似的框架，你应该能理解根据不同条件拼接 SQL 语句有多痛苦，例如拼接时要确保不能忘记添加必要的空格，还要注意去掉列表最后一个列名的逗号。利用动态 SQL，可以彻底摆脱这种痛苦
- [MyBatis详解 - 插件机制](MyBatis详解 - 插件机制.md)
  - MyBatis提供了一种插件(plugin)的功能，虽然叫做插件，但其实这是拦截器功能。那么拦截器拦截MyBatis中的哪些内容呢？
- [MyBatis详解 - 插件之分页机制](MyBatis详解 - 插件之分页机制.md)
  - Mybatis的分页功能很弱，它是基于内存的分页（查出所有记录再按偏移量和limit取结果），在大数据量的情况下这样的分页基本上是没有用的。本文基于插件，通过拦截StatementHandler重写sql语句，实现数据库的物理分页
- [MyBatis详解 - 数据源与连接池](MyBatis详解 - 数据源与连接池.md)
  - 本文主要介绍MyBatis数据源和连接池相关的内容。
- [MyBatis详解 - 事务管理机制](MyBatis详解 - 事务管理机制.md)
  - 本文主要介绍MyBatis事务管理相关的使用和机制。
- [MyBatis详解 - 一级缓存实现机制](MyBatis详解 - 一级缓存实现机制.md)
  - 减少资源的浪费，MyBatis会在表示会话的SqlSession对象中建立一个简单的缓存，将每次查询到的结果结果缓存起来，当下次查询的时候，如果判断先前有个完全一样的查询，会直接从缓存中直接将结果取出，返回给用户，不需要再进行一次数据库查询了。
- [MyBatis详解 - 二级缓存实现机制](MyBatis详解 - 二级缓存实现机制.md)
  - MyBatis的二级缓存是Application级别的缓存，它可以提高对数据库查询的效率，以提高应用的性能。

## 参考资料

注：Mybatis系列：

- 第一版，作者为 CSDN博主栾山，网址是https://louluan.blog.csdn.net/
- 第二版，陶邦仁在此基础上做了整理和补充 https://my.oschina.net/xianggao/blog/591482
- 当前版本，pdai在上述两版本基础上进行了进一步的整理和补充
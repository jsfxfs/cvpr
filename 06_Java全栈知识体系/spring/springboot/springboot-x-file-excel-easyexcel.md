# SpringBoot集成文件 - 集成EasyExcel之Excel导入导出

> EasyExcel是一个基于Java的、快速、简洁、解决大文件内存溢出的Excel处理工具。它能让你在不用考虑性能、内存的等因素的情况下，快速完成Excel的读、写等功能。它是基于POI来封装实现的，主要解决其易用性，封装性和性能问题。本文主要介绍通过SpringBoot集成Excel实现Excel的导入，导出和填充模板等功能。@pdai

## 知识准备

> 需要了解EasyExcel，以及这个工具设计的初衷（为什么有了POI，还会需要EasyExcel?)。

### 什么是EasyExcel

> EasyExcel是阿里开源的基于POI封装的Excel处理工具，更多请参考[官方文档](https://poi.apache.org/index.html)。

EasyExcel是一个基于Java的、快速、简洁、解决大文件内存溢出的Excel处理工具。它能让你在不用考虑性能、内存的等因素的情况下，快速完成Excel的读、写等功能。

### EasyExcel要解决POI什么问题？

> 因为EasyExcel是基于POI封装的，主要考虑的是易用性，封装性和性能问题。

Java解析、生成Excel比较有名的框架有Apache poi、jxl。但他们都存在一个严重的问题就是非常的耗内存，poi有一套SAX模式的API可以一定程度的解决一些内存溢出的问题，但POI还是有一些缺陷，比如07版Excel解压缩以及解压后存储都是在内存中完成的，内存消耗依然很大。easyexcel重写了poi对07版Excel的解析，一个3M的excel用POI sax解析依然需要100M左右内存，改用easyexcel可以降低到几M，并且再大的excel也不会出现内存溢出；03版依赖POI的sax模式，在上层做了模型转换的封装，让使用者更加简单方便。

## 实现案例

> 这里展示SpringBoot集成EasyExcel导出用户列表的和导入用户列表的例子。

### Pom依赖

引入poi的依赖包

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>easyexcel</artifactId>
    <version>3.1.1</version>
</dependency>
```

### 导出Excel

User类

```java
package tech.pdai.springboot.file.excel.easyexcel.entity;

import com.alibaba.excel.annotation.ExcelProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author pdai
 */
@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class User implements BaseEntity {

    /**
     * user id.
     */
    @ExcelProperty("ID")
    private Long id;

    /**
     * username.
     */
    @ExcelProperty("Name")
    private String userName;

    /**
     * email.
     */
    @ExcelProperty("Email")
    private String email;

    /**
     * phoneNumber.
     */
    @ExcelProperty("Phone")
    private long phoneNumber;

    /**
     * description.
     */
    @ExcelProperty("Description")
    private String description;

}
```

UserController中导出的方法

```java
@ApiOperation("Download Excel")
@GetMapping("/excel/download")
public void download(HttpServletResponse response) {
    try {
        response.reset();
        response.setContentType("application/vnd.ms-excel");
        response.setHeader("Content-disposition",
                "attachment;filename=user_excel_" + System.currentTimeMillis() + ".xlsx");
        userService.downloadExcel(response.getOutputStream());
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

UserServiceImple中导出Excel的主方法(是不是很简洁)

```java
@Override
public void downloadExcel(ServletOutputStream outputStream) {
    EasyExcelFactory.write(outputStream, User.class).sheet("User").doWrite(this::getUserList);
}
private List<User> getUserList() {
    return Collections.singletonList(User.builder()
            .id(1L).userName("pdai").email("pdai@pdai.tech").phoneNumber(121231231231L)
            .description("hello world")
            .build());
}
```

导出后的excel如下

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easyexcel-1.png)

### 导入Excel

> 我们将上面导出的excel文件导入。

UserController中导入的方法

```java
@ApiOperation("Upload Excel")
@PostMapping("/excel/upload")
public ResponseResult<String> upload(@RequestParam(value = "file", required = true) MultipartFile file) {
    try {
        userService.upload(file.getInputStream());
    } catch (Exception e) {
        e.printStackTrace();
        return ResponseResult.fail(e.getMessage());
    }
    return ResponseResult.success();
}
```

UserServiceImple中导入Excel的主方法

```java
@Override
public void upload(InputStream inputStream) throws IOException {
    // ReadListener不是必须的，它主要的设计是读取excel数据的后置处理(并考虑一次性读取到内存潜在的内存泄漏问题)
    EasyExcelFactory.read(inputStream, User.class, new ReadListener<User>() {

        @Override
        public void invoke(User user, AnalysisContext analysisContext) {
            cachedDataList.add(user);
        }

        @Override
        public void doAfterAllAnalysed(AnalysisContext analysisContext) {
            cachedDataList.forEach(user -> log.info(user.toString()));
        }
    }).sheet().doRead();
}
```

通过PostMan进行接口测试

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easyexcel-2.png)

这里注意下，需要有字体的支持，比如如果没有字体支撑将会报如下告警：

```java
Warning: the font "Times" is not available, so "Lucida Bright" has been substituted, but may have unexpected appearance or behavor. Re-enable the "Times" font to remove this warning.
```

### 填充Excel模板

我们先来准备一个excel模板，考虑了横向表和纵向列表，以及单一信息等，基本上能满足多数的应用场景。

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easyexcel-4.png)

UserController中下载填充后的Excel方法

```java
@ApiOperation("Fill Excel Template")
@GetMapping("/excel/fill")
public void fillTemplate(HttpServletResponse response) {
    try {
        response.reset();
        response.setContentType("application/vnd.ms-excel");
        response.setHeader("Content-disposition",
                "attachment;filename=user_excel_template_" + System.currentTimeMillis() + ".xlsx");
        userService.fillExcelTemplate(response.getOutputStream());
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

UserServiceImpl中填充excel模板的方法

```java
// 模板注意 用{} 来表示你要用的变量 如果本来就有"{","}" 特殊字符 用"\{","\}"代替
// {} 代表普通变量 {.} 代表是list的变量 {前缀.} 前缀可以区分不同的list
@Override
public void fillExcelTemplate(ServletOutputStream outputStream) {

    // 确保文件可访问，这个例子的excel模板，放在根目录下面
    String templateFileName = "/Users/pdai/Downloads/user_excel_template.xlsx";

    // 方案1
    try (ExcelWriter excelWriter = EasyExcelFactory.write(outputStream).withTemplate(templateFileName).build()) {
        WriteSheet writeSheet = EasyExcelFactory.writerSheet().build();
        FillConfig fillConfig = FillConfig.builder().direction(WriteDirectionEnum.HORIZONTAL).build();
        // 如果有多个list 模板上必须有{前缀.} 这里的前缀就是 userList，然后多个list必须用 FillWrapper包裹
        excelWriter.fill(new FillWrapper("userList", getUserList()), fillConfig, writeSheet);
        excelWriter.fill(new FillWrapper("userList", getUserList()), fillConfig, writeSheet);

        excelWriter.fill(new FillWrapper("userList2", getUserList()), writeSheet);
        excelWriter.fill(new FillWrapper("userList2", getUserList()), writeSheet);

        Map<String, Object> map = new HashMap<>();
        map.put("user", "pdai");
        map.put("date", new Date());

        excelWriter.fill(map, writeSheet);
    }
}
```

访问http://localhost:8080/user/excel/fill 下载

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easyexcel-3.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos

## 参考文章

https://easyexcel.opensource.alibaba.com/docs/current/
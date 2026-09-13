# SpringBoot集成文件 - 集成EasyPOI之Excel导入导出

> 除了POI和EasyExcel，国内还有一个EasyPOI框架较为常见，适用于没有使用过POI并希望快速操作Excel的入门项目，在中大型项目中并不推荐使用(为了保证知识体系的完整性，把EasyPOI也加了进来)。本文主要介绍SpringBoot集成EasyPOI实现Excel的导入，导出和填充模板等功能。@pdai

## 知识准备

> 需要对EasyPOI特色功能和潜在缺陷。@pdai

### 什么是EasyPOI

> 如下是[EasyPOI官方](http://doc.wupaas.com/docs/easypoi/easypoi-1c0u4mo8p4ro8)介绍的功能。

独特的功能：

- 基于注解的导入导出,修改注解就可以修改Excel
- 支持常用的样式自定义
- 基于map可以灵活定义的表头字段
- 支持一堆多的导出,导入
- 支持模板的导出,一些常见的标签,自定义标签
- 支持HTML/Excel转换,如果模板还不能满足用户的变态需求,请用这个功能
- 支持word的导出,支持图片,Excel

### 如何看待EasyPOI

> **不建议在稍复杂的项目中使用EasyPOI**。@pdai

- 简单的功能通过对POI的封装成本也不高，复杂的一点的适配性差；有点像为了做某件事方便，引入了一个工具，最后发现大量的时间都在迎合/修理这个工具
- 个人色彩，缺少稳定维护团队，潜在风险远大于节约的这点时间；同时个人开源又期望寻求盈利点，对开发者选择而言是要很慎重的。
- 封装的思路可以借鉴下，在自行根据业务封装时可以参考下

## 实现案例

> 这里展示SpringBoot集成EasyPOI导出用户列表的和导入用户列表的例子。

### Pom依赖

引入poi的依赖包

```xml
<dependency>
    <groupId>cn.afterturn</groupId>
    <artifactId>easypoi-spring-boot-starter</artifactId>
    <version>4.4.0</version>
</dependency>
```

### 导出Excel

User 类

```java
package tech.pdai.springboot.file.excel.easypoi.entity;

import cn.afterturn.easypoi.excel.annotation.Excel;
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
    @Excel(name = "ID")
    private Long id;

    /**
     * username.
     */
    @Excel(name = "Name")
    private String userName;

    /**
     * email.
     */
    @Excel(name = "Email")
    private String email;

    /**
     * phoneNumber.
     */
    @Excel(name = "Phone")
    private long phoneNumber;

    /**
     * description.
     */
    @Excel(name = "Description")
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

UserServiceImple中导出Excel的主方法

```java
@Override
public void downloadExcel(ServletOutputStream outputStream) throws IOException {
    ExportParams exportParams = new ExportParams();
    exportParams.setTitle("User Table");
    exportParams.setSheetName("User Sheet");
    Workbook workbook = ExcelExportUtil.exportExcel(exportParams, User.class, getUserList());
    workbook.write(outputStream);
    workbook.close();
}
```

导出后的excel如下

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easypoi-1.png)

> PS：再吐槽下：

当getUserList用 Collections.singletonList时是直接报错，看了下源码~

```java
private List<User> getUserList() {
    return Collections.singletonList(User.builder()
            .id(1L).userName("pdai").email("pdai@pdai.tech").phoneNumber(121231231231L)
            .description("hello world")
            .build());
}
```

默默改成ArrayList, 因为源代码是通过remove来迭代的，且只对Unmodified Collection做了处理，而没有对singletonList... 只能说不建议在稍复杂的项目中使用EasyPOI...

```java
private List<User> getUserList() {
    List<User> userList = new ArrayList<>();
    userList.add(User.builder()
            .id(1L).userName("pdai").email("pdai@pdai.tech").phoneNumber(121231231231L)
            .description("hello world")
            .build());
    return userList;
}
```

### 导入Excel

UserController中导入的方法，（导入的文件在项目根目录）

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
public void upload(InputStream inputStream) throws Exception {
    ImportParams importParams = new ImportParams();
    List<User> userList = ExcelImportUtil.importExcel(inputStream, User.class, importParams);
    userList.stream().forEach(user -> log.info(user.toString()));
}
```

通过PostMan进行接口测试

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easypoi-2.png)

日志如下

```java
2022-06-15 22:20:48.145  INFO 52348 --- [nio-8080-exec-2] t.p.s.f.e.e.s.impl.UserServiceImpl       : User(id=1, userName=pdai, email=pdai@pdai.tech, phoneNumber=121231231231, description=hello world)
```

### 填充Excel模板

准备如下Excel模板

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easypoi-3.png)

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
@Override
public void fillExcelTemplate(ServletOutputStream outputStream) throws IOException {
    // 确保文件可访问，这个例子的excel模板，放在根目录下面
    String templateFileName = "/Users/pdai/Downloads/user_excel_template_easypoi.xlsx";
    TemplateExportParams params = new TemplateExportParams(templateFileName);

    Map<String, Object> map = new HashMap<>();
    map.put("user", "pdai");
    map.put("date", new Date());
    map.put("userList", getUserList());
    Workbook workbook = ExcelExportUtil.exportExcel(params, map);
    workbook.write(outputStream);
    workbook.close();
}

private List<User> getUserList() {
    List<User> userList = new ArrayList<>();
    userList.add(User.builder()
            .id(1L).userName("pdai").email("pdai@pdai.tech").phoneNumber(121231231231L)
            .description("hello world")
            .build());
    userList.add(User.builder()
            .id(2L).userName("pdai2").email("pdai2@pdai.tech").phoneNumber(1212312312312L)
            .description("hello world2")
            .build());
    return userList;
}
```

访问http://localhost:8080/user/excel/fill 下载

![](https://www.pdai.tech/images/spring/springboot/springboot-file-excel-easypoi-4.png)

(PS: 说实在的，稍复杂一些的，不如自己封装...)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos

## 参考文章

http://doc.wupaas.com/docs/easypoi/easypoi-1c0u4mo8p4ro8
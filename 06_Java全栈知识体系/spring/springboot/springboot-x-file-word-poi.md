# SpringBoot集成文件 - 集成POI之Word导出

> 前文我们介绍了通过Apache POI导出excel，而Apache POI包含是操作Office Open XML（OOXML）标准和微软的OLE 2复合文档格式（OLE2）的Java API。所以也是可以通过POI来导出word的。本文主要介绍通过SpringBoot集成POI工具实现Word的导出功能。@pdai

## 知识准备

> 需要理解Apache POI遵循的标准（Office Open XML（OOXML）标准和微软的OLE 2复合文档格式（OLE2））， 这将对应着API的依赖包。@pdai

### 什么是POI

> Apache POI 是用Java编写的免费开源的跨平台的 Java API，Apache POI提供API给Java程序对Microsoft Office格式档案读和写的功能。POI为“Poor Obfuscation Implementation”的首字母缩写，意为“简洁版的模糊实现”。

Apache POI 是创建和维护操作各种符合Office Open XML（OOXML）标准和微软的OLE 2复合文档格式（OLE2）的Java API。更多请参考[官方文档](https://poi.apache.org/index.html)。

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-1.png)

## 实现案例

> 这里展示SpringBoot集成POI导出用户信息的Word例子。

### Pom依赖

引入poi的依赖包

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.2</version>
</dependency>
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.2</version>
</dependency>
```

### 导出Word

UserController中导出的方法

```java
package tech.pdai.springboot.file.word.poi.controller;


import java.io.OutputStream;

import javax.servlet.http.HttpServletResponse;

import io.swagger.annotations.ApiOperation;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.springboot.file.word.poi.service.IUserService;

/**
 * @author pdai
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private IUserService userService;

    @ApiOperation("Download Word")
    @GetMapping("/word/download")
    public void download(HttpServletResponse response) {
        try {
            XWPFDocument document = userService.generateWordXWPFDocument();
            response.reset();
            response.setContentType("application/vnd.ms-excel");
            response.setHeader("Content-disposition",
                    "attachment;filename=user_world_" + System.currentTimeMillis() + ".docx");
            OutputStream os = response.getOutputStream();
            document.write(os);
            os.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
```

UserServiceImple中导出Word方法

```java
package tech.pdai.springboot.file.word.poi.service.impl;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

import lombok.extern.slf4j.Slf4j;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.util.Units;
import org.apache.poi.xwpf.usermodel.BreakType;
import org.apache.poi.xwpf.usermodel.Document;
import org.apache.poi.xwpf.usermodel.ParagraphAlignment;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.apache.poi.xwpf.usermodel.XWPFRun;
import org.apache.poi.xwpf.usermodel.XWPFTable;
import org.apache.poi.xwpf.usermodel.XWPFTableCell;
import org.openxmlformats.schemas.wordprocessingml.x2006.main.CTTblPr;
import org.openxmlformats.schemas.wordprocessingml.x2006.main.CTTblWidth;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.file.word.poi.entity.User;
import tech.pdai.springboot.file.word.poi.service.IUserService;

/**
 * @author pdai
 */
@Slf4j
@Service
public class UserServiceImpl implements IUserService {

    @Override
    public XWPFDocument generateWordXWPFDocument() {
        XWPFDocument doc = new XWPFDocument();

        // Title
        createTitle(doc, "Java 全栈知识体系");

        // Chapter 1
        createChapterH1(doc, "1. 知识准备");
        createChapterH2(doc, "1.1 什么是POI");
        createParagraph(doc, "Apache POI 是创建和维护操作各种符合Office Open XML（OOXML）标准和微软的OLE 2复合文档格式（OLE2）的Java API。用它可以使用Java读取和创建,修改MS Excel文件.而且,还可以使用Java读取和创建MS Word和MSPowerPoint文件。更多请参考[官方文档](https://poi.apache.org/index.html)");
        createChapterH2(doc, "1.2 POI中基础概念");
        createParagraph(doc, "生成xls和xlsx有什么区别？POI对Excel中的对象的封装对应关系？");

        // Chapter 2
        createChapterH1(doc, "2. 实现案例");
        createChapterH2(doc, "2.1 用户列表示例");
        createParagraph(doc, "以导出用户列表为例");

        // 表格
        List<User> userList = getUserList();
        XWPFParagraph paragraph = doc.createParagraph();
        XWPFTable table = paragraph.getDocument().createTable(userList.size(), 5);
        table.setWidth(500);
        table.setCellMargins(20, 20, 20, 20);

        //表格属性
        CTTblPr tablePr = table.getCTTbl().addNewTblPr();
        //表格宽度
        CTTblWidth width = tablePr.addNewTblW();
        width.setW(BigInteger.valueOf(8000));

        for(int i = 0; i< userList.size(); i++) {
            List<XWPFTableCell> tableCells = table.getRow(i).getTableCells();
            tableCells.get(0).setText(userList.get(i).getId()+"");
            tableCells.get(1).setText(userList.get(i).getUserName());
            tableCells.get(2).setText(userList.get(i).getEmail());
            tableCells.get(3).setText(userList.get(i).getPhoneNumber()+"");
            tableCells.get(4).setText(userList.get(i).getDescription());
        }

        createChapterH2(doc, "2.2 图片导出示例");
        createParagraph(doc, "以导出图片为例");
        // 图片
        InputStream stream = null;
        try {
            XWPFParagraph paragraph2 = doc.createParagraph();
            Resource resource = new ClassPathResource("pdai-guli.png");
            stream = new FileInputStream(resource.getFile());
            XWPFRun run = paragraph2.createRun();
            run.addPicture(stream, Document.PICTURE_TYPE_PNG, "Generated", Units.toEMU(256), Units.toEMU(256));
        } catch (IOException | InvalidFormatException e) {
            e.printStackTrace();
        }

        return doc;
    }

    private void createTitle(XWPFDocument doc, String content) {
        XWPFParagraph title = doc.createParagraph();
        title.setAlignment(ParagraphAlignment.CENTER);
        XWPFRun r1 = title.createRun();
        r1.setBold(true);
        r1.setFontFamily("宋体");
        r1.setText(content);
        r1.setFontSize(22);
    }

    private void createChapterH1(XWPFDocument doc, String content) {
        XWPFParagraph actTheme = doc.createParagraph();
        actTheme.setAlignment(ParagraphAlignment.LEFT);
        XWPFRun runText1 = actTheme.createRun();
        runText1.setBold(true);
        runText1.setText(content);
        runText1.setFontSize(18);
    }

    private void createChapterH2(XWPFDocument doc, String content) {
        XWPFParagraph actType = doc.createParagraph();
        XWPFRun runText2 = actType.createRun();
        runText2.setBold(true);
        runText2.setText(content);
        runText2.setFontSize(15);
    }

    private void createParagraph(XWPFDocument doc, String content) {
        XWPFParagraph actType = doc.createParagraph();
        XWPFRun runText2 = actType.createRun();
        runText2.setText(content);
        runText2.setFontSize(11);
    }

    private List<User> getUserList() {
        List<User> userList = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            userList.add(User.builder()
                    .id(Long.parseLong(i + "")).userName("pdai" + i).email("pdai@pdai.tech" + i).phoneNumber(121231231231L)
                    .description("hello world" + i)
                    .build());
        }
        return userList;
    }

}
```

导出

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-2.png)

导出后的word

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-3.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos

## 参考文档

https://poi.apache.org/index.html
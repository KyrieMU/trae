# SQL入门教程

## 1. 数据库基础概念

### 1.1 什么是数据库？
数据库是一个有组织的数据集合，它以一定方式存储在计算机中，可以被多个用户共享和使用。

### 1.2 基本概念
- **表（Table）**：数据库中存储数据的基本单位
- **行（Row）**：表中的一条记录
- **列（Column）**：表中的一个字段
- **主键（Primary Key）**：唯一标识表中每条记录的字段

## 2. 基本SQL语句

### 2.1 SELECT语句 - 查询数据
```sql
-- 基本查询
SELECT * FROM 表名;

-- 指定列查询
SELECT 列名1, 列名2 FROM 表名;
```

### 2.2 INSERT语句 - 插入数据
```sql
-- 插入单条数据
INSERT INTO 表名 (列名1, 列名2) VALUES (值1, 值2);

-- 插入多条数据
INSERT INTO 表名 (列名1, 列名2) VALUES 
(值1, 值2),
(值3, 值4);
```

### 2.3 UPDATE语句 - 更新数据
```sql
-- 更新数据
UPDATE 表名
SET 列名1 = 新值1, 列名2 = 新值2
WHERE 条件;
```

### 2.4 DELETE语句 - 删除数据
```sql
-- 删除数据
DELETE FROM 表名 WHERE 条件;
```

## 3. 进阶查询技巧

### 3.1 WHERE子句 - 条件筛选
```sql
-- 等值查询
SELECT * FROM 表名 WHERE 列名 = 值;

-- 范围查询
SELECT * FROM 表名 WHERE 列名 BETWEEN 值1 AND 值2;

-- 模糊查询
SELECT * FROM 表名 WHERE 列名 LIKE '%关键字%';
```

### 3.2 ORDER BY - 排序
```sql
-- 升序排序
SELECT * FROM 表名 ORDER BY 列名 ASC;

-- 降序排序
SELECT * FROM 表名 ORDER BY 列名 DESC;
```

### 3.3 GROUP BY - 分组
```sql
-- 分组统计
SELECT 列名, COUNT(*) as 数量
FROM 表名
GROUP BY 列名;
```

## 4. 多表操作

### 4.1 表关系
- 一对一关系
- 一对多关系
- 多对多关系

### 4.2 JOIN连接查询
```sql
-- 内连接
SELECT * FROM 表1
INNER JOIN 表2 ON 表1.列名 = 表2.列名;

-- 左连接
SELECT * FROM 表1
LEFT JOIN 表2 ON 表1.列名 = 表2.列名;

-- 右连接
SELECT * FROM 表1
RIGHT JOIN 表2 ON 表1.列名 = 表2.列名;
```

## 5. 实践案例：图书管理系统

### 5.1 创建数据库和表
```sql
-- 创建图书表
CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(50),
    price DECIMAL(10,2),
    stock INT
);

-- 创建读者表
CREATE TABLE readers (
    reader_id INT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(20)
);

-- 创建借阅记录表
CREATE TABLE borrowings (
    id INT PRIMARY KEY,
    book_id INT,
    reader_id INT,
    borrow_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (reader_id) REFERENCES readers(reader_id)
);
```

### 5.2 基本操作示例
```sql
-- 添加图书
INSERT INTO books VALUES (1, '数据库系统概论', '王珊', 59.00, 10);

-- 添加读者
INSERT INTO readers VALUES (1, '张三', '13800138000');

-- 记录借阅
INSERT INTO borrowings VALUES (1, 1, 1, '2024-03-14', NULL);

-- 查询借阅信息
SELECT b.title, r.name, br.borrow_date
FROM borrowings br
INNER JOIN books b ON br.book_id = b.book_id
INNER JOIN readers r ON br.reader_id = r.reader_id;
```

### 5.3 练习题
1. 查询所有未归还的图书
2. 统计每本书被借阅的次数
3. 查询借阅次数最多的读者
4. 计算每个读者的借阅历史

## 6. 学习建议
1. 多动手实践，可以使用在线SQL编辑器进行练习
2. 从简单查询开始，逐步过渡到复杂查询
3. 理解表之间的关系，这对后续学习很重要
4. 养成良好的SQL编写习惯，注意代码的可读性

## 7. 常用在线资源
- [SQL在线练习平台](https://www.w3schools.com/sql/)
- [菜鸟教程SQL教程](https://www.runoob.com/sql/sql-tutorial.html)
- [LeetCode数据库题目](https://leetcode.com/problemset/database/)
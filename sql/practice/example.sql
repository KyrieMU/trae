-- 这是一个示例SQL文件
-- 用于演示如何组织SQL代码

-- 创建一个简单的用户表
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入示例数据
INSERT INTO users (id, username, email) VALUES
(1, 'user1', 'user1@example.com'),
(2, 'user2', 'user2@example.com');

-- 查询示例
SELECT * FROM users WHERE id > 1;
// 获取画布和上下文
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreElement = document.getElementById("score");

// 游戏参数
let score = 0;
let lives = 3;
let level = 1;
let gameOver = false;
let gamePaused = false;
let gameStarted = false;

// 球的参数
const ball = {
    x: canvas.width / 2,
    y: canvas.height - 30,
    radius: 10,
    dx: 4,
    dy: -4,
    color: "#0095DD"
};

// 挡板参数
const paddle = {
    width: 80,
    height: 10,
    x: (canvas.width - 80) / 2,
    y: canvas.height - 20,
    color: "#0095DD",
    speed: 8
};

// 砖块参数
const brickRowCount = 5;
const brickColumnCount = 8;
const brickWidth = 50;
const brickHeight = 20;
const brickPadding = 10;
const brickOffsetTop = 60;
const brickOffsetLeft = 25;

// 创建砖块数组
const bricks = [];
for (let c = 0; c < brickColumnCount; c++) {
    bricks[c] = [];
    for (let r = 0; r < brickRowCount; r++) {
        // 根据行数设置不同的颜色和分数
        let color;
        let points;
        switch (r) {
            case 0:
                color = "#FF5252"; // 红色
                points = 5;
                break;
            case 1:
                color = "#FF9800"; // 橙色
                points = 4;
                break;
            case 2:
                color = "#FFEB3B"; // 黄色
                points = 3;
                break;
            case 3:
                color = "#4CAF50"; // 绿色
                points = 2;
                break;
            case 4:
                color = "#2196F3"; // 蓝色
                points = 1;
                break;
        }
        
        bricks[c][r] = { 
            x: 0, 
            y: 0, 
            status: 1, 
            color: color,
            points: points
        };
    }
}

// 键盘控制
const keys = {
    right: false,
    left: false
};

// 事件监听
document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);
canvas.addEventListener("mousemove", mouseMoveHandler);
document.addEventListener("click", startGame);

// 触摸事件支持
canvas.addEventListener("touchstart", touchHandler);
canvas.addEventListener("touchmove", touchHandler);

function touchHandler(e) {
    if (!gameStarted) {
        startGame();
    }
    
    if (e.touches) {
        const relativeX = e.touches[0].clientX - canvas.offsetLeft;
        if (relativeX > 0 && relativeX < canvas.width) {
            paddle.x = relativeX - paddle.width / 2;
        }
    }
    
    e.preventDefault();
}

function keyDownHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        keys.right = true;
    } else if (e.key === "Left" || e.key === "ArrowLeft") {
        keys.left = true;
    } else if (e.key === "p" || e.key === "P") {
        togglePause();
    } else if (e.key === " " && !gameStarted) {
        startGame();
    } else if (e.key === "r" || e.key === "R") {
        if (gameOver) resetGame();
    }
}

function keyUpHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        keys.right = false;
    } else if (e.key === "Left" || e.key === "ArrowLeft") {
        keys.left = false;
    }
}

function mouseMoveHandler(e) {
    const relativeX = e.clientX - canvas.offsetLeft;
    if (relativeX > 0 && relativeX < canvas.width) {
        paddle.x = relativeX - paddle.width / 2;
    }
}

function togglePause() {
    gamePaused = !gamePaused;
    if (!gamePaused) {
        draw();
    }
}

function startGame() {
    if (!gameStarted && !gameOver) {
        gameStarted = true;
        draw();
    }
}

function resetGame() {
    score = 0;
    lives = 3;
    level = 1;
    gameOver = false;
    gameStarted = false;
    
    ball.x = canvas.width / 2;
    ball.y = canvas.height - 30;
    ball.dx = 4;
    ball.dy = -4;
    
    paddle.x = (canvas.width - paddle.width) / 2;
    
    // 重置砖块
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r].status = 1;
        }
    }
    
    scoreElement.textContent = score;
    drawStartScreen();
}

// 碰撞检测
function collisionDetection() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            const brick = bricks[c][r];
            if (brick.status === 1) {
                if (
                    ball.x > brick.x &&
                    ball.x < brick.x + brickWidth &&
                    ball.y > brick.y &&
                    ball.y < brick.y + brickHeight
                ) {
                    ball.dy = -ball.dy;
                    brick.status = 0;
                    score += brick.points;
                    scoreElement.textContent = score;
                    
                    // 检查是否所有砖块都被击中
                    if (checkLevelComplete()) {
                        level++;
                        nextLevel();
                    }
                }
            }
        }
    }
}

function checkLevelComplete() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            if (bricks[c][r].status === 1) {
                return false;
            }
        }
    }
    return true;
}

function nextLevel() {
    // 增加难度
    ball.dx *= 1.1;
    ball.dy *= 1.1;
    
    // 重置球和挡板位置
    ball.x = canvas.width / 2;
    ball.y = canvas.height - 30;
    paddle.x = (canvas.width - paddle.width) / 2;
    
    // 重置砖块
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r].status = 1;
        }
    }
    
    // 短暂暂停
    gamePaused = true;
    setTimeout(() => {
        gamePaused = false;
        draw();
    }, 1000);
}

// 绘制球
function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = ball.color;
    ctx.fill();
    ctx.closePath();
}

// 绘制挡板
function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddle.x, paddle.y, paddle.width, paddle.height);
    ctx.fillStyle = paddle.color;
    ctx.fill();
    ctx.closePath();
}

// 绘制砖块
function drawBricks() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            if (bricks[c][r].status === 1) {
                const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                
                ctx.beginPath();
                ctx.rect(brickX, brickY, brickWidth, brickHeight);
                ctx.fillStyle = bricks[c][r].color;
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

// 绘制分数和生命值
function drawStats() {
    // 绘制等级
    ctx.font = "16px Arial";
    ctx.fillStyle = "#FFFFFF";
    ctx.fillText(`等级: ${level}`, 8, 20);
    
    // 绘制生命值
    ctx.font = "16px Arial";
    ctx.fillStyle = "#FFFFFF";
    ctx.fillText(`生命: ${lives}`, canvas.width - 80, 20);
}

// 绘制开始屏幕
function drawStartScreen() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBricks();
    drawPaddle();
    drawBall();
    
    ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.font = "30px Arial";
    ctx.fillStyle = "#FFFFFF";
    ctx.textAlign = "center";
    ctx.fillText("弹球打砖块", canvas.width / 2, canvas.height / 2 - 50);
    
    ctx.font = "20px Arial";
    ctx.fillText("点击或按空格键开始游戏", canvas.width / 2, canvas.height / 2);
    ctx.fillText("使用鼠标或方向键移动挡板", canvas.width / 2, canvas.height / 2 + 30);
    ctx.fillText("按 P 键暂停游戏", canvas.width / 2, canvas.height / 2 + 60);
    
    ctx.textAlign = "left";
}

// 绘制游戏结束屏幕
function drawGameOver() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.font = "30px Arial";
    ctx.fillStyle = "#FFFFFF";
    ctx.textAlign = "center";
    ctx.fillText("游戏结束", canvas.width / 2, canvas.height / 2 - 50);
    
    ctx.font = "20px Arial";
    ctx.fillText(`最终分数: ${score}`, canvas.width / 2, canvas.height / 2);
    ctx.fillText(`达到等级: ${level}`, canvas.width / 2, canvas.height / 2 + 30);
    ctx.fillText("按 R 键重新开始", canvas.width / 2, canvas.height / 2 + 60);
    
    ctx.textAlign = "left";
}

// 绘制暂停屏幕
function drawPauseScreen() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.font = "30px Arial";
    ctx.fillStyle = "#FFFFFF";
    ctx.textAlign = "center";
    ctx.fillText("游戏暂停", canvas.width / 2, canvas.height / 2);
    ctx.font = "20px Arial";
    ctx.fillText("按 P 键继续", canvas.width / 2, canvas.height / 2 + 40);
    
    ctx.textAlign = "left";
}

// 主绘制函数
function draw() {
    if (gameOver) {
        drawGameOver();
        return;
    }
    
    if (!gameStarted) {
        drawStartScreen();
        return;
    }
    
    if (gamePaused) {
        drawPauseScreen();
        return;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBricks();
    drawBall();
    drawPaddle();
    drawStats();
    collisionDetection();
    
    // 球碰到墙壁反弹
    if (ball.x + ball.dx > canvas.width - ball.radius || ball.x + ball.dx < ball.radius) {
        ball.dx = -ball.dx;
    }
    
    // 球碰到顶部反弹
    if (ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    } 
    // 球碰到底部
    else if (ball.y + ball.dy > canvas.height - ball.radius) {
        // 检查是否碰到挡板
        if (ball.x > paddle.x && ball.x < paddle.x + paddle.width) {
            // 根据球击中挡板的位置改变反弹角度
            let hitPoint = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2);
            ball.dx = hitPoint * 5; // 根据击中位置调整水平速度
            ball.dy = -ball.dy;
        } else {
            lives--;
            if (lives === 0) {
                gameOver = true;
            } else {
                ball.x = canvas.width / 2;
                ball.y = canvas.height - 30;
                ball.dx = 4;
                ball.dy = -4;
                paddle.x = (canvas.width - paddle.width) / 2;
            }
        }
    }
    
    // 更新球的位置
    ball.x += ball.dx;
    ball.y += ball.dy;
    
    // 更新挡板位置
    if (keys.right && paddle.x < canvas.width - paddle.width) {
        paddle.x += paddle.speed;
    } else if (keys.left && paddle.x > 0) {
        paddle.x -= paddle.speed;
    }
    
    // 继续动画
    if (!gameOver) {
        requestAnimationFrame(draw);
    }
}

// 初始化游戏
drawStartScreen();
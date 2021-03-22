const cvs = document.getElementById('snake');
const ctx = cvs.getContext('2d');
const square = 20;
const snakeContainer = document.getElementById("snake")

var direcX, direcY;
var interval;
var snake = [];
var directionY = 0;
var directionX = -1;
var speed = document.getElementById("speed").value;
var height = cvs.height,
    width = cvs.width;
var length = 4;
var fruit = {};




function setUp() {
    initWindow();
    eventListerners();
    randomFruit();
}
setUp();

function makeSnake() {
    length = 4;
    snake = [];
    snake[0] = {
        x: 5 * square,
        y: 5 * square
    };
    for (let i = 1; i < length; i++) {
        snake[i] = {
            x: snake[i - 1].x + square,
            y: snake[i - 1].y
        }
    }
}

function randomFruit() {
    let x = Math.floor((Math.random() * (width - square)) + 0);
    let y = Math.floor((Math.random() * (height - square)) + 0);
    y = (square - (y % square)) + y;
    x = (square - (x % square)) + x;

    let test = {
        x: x,
        y: y
    }

    let bool = doesInclude(test);

    if (bool) {
        randomFruit();
    } else {
        fruit = test;
    }
}

function paintSnake() {
    direcX = directionX;
    direcY = directionY;
    snake.unshift({
        x: snake[0].x + direcX * square,
        y: snake[0].y + direcY * square
    });

    if (snake[0].x == fruit.x && snake[0].y == fruit.y) {
        length++;
        randomFruit();
    }

    snake = snake.slice(0, length);
    if (touchedItself()) {
        stopSnake();
        return;
    }
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#69FE36";
    ctx.fillRect(0, 0, 300, 300);
    for (let i = 0; i < snake.length; i++) {
        if (i == 0) {
            ctx.strokeRect(snake[i].x, snake[i].y, square, square);
        }
        ctx.fillStyle = 'blue';
        ctx.fillRect(snake[i].x, snake[i].y, square, square);
    }
    ctx.fillStyle = 'red';
    ctx.fillRect(fruit.x, fruit.y, square, square);
    ctx.stroke();
    if (hitBorder()) {
        stopSnake();
        return;
    }
}

function start() {
    document.getElementById("finished").style.display = "none"
    speed = document.getElementById("speed").value;
    snakeContainer.classList.remove("stoped")
    directionX = -1;
    directionY = 0;
    console.log("start");
    makeSnake();
    interval = setInterval(paintSnake, 500 / speed);
    randomFruit();
}

function initWindow() {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#2E4CA4";
    ctx.fillRect(0, 0, width, height);
    ctx.font = "bold 20px Ubuntu";
    ctx.fillStyle = "white";
    ctx.fillText("click to start the game", 40, height/2);
    snakeContainer.classList.add("stoped")
}

function doesInclude(value) {
    for (let i = 0; i < snake.length; i++) {
        if (value.x == snake[i].x && value.y == snake[i].y) {
            return true;
        }
    }
    return false;
}


function stopSnake() {
    clearInterval(interval);
    ctx.clearRect(0, 0, width, height);
    ctx.font = "bold 20px Ubuntu";
    ctx.fillStyle = "white";
    ctx.fillText("Game Over, your score was " + (length - 4), 20, height/2);

    document.getElementById("finished").style.display = "inherit"
    snakeContainer.classList.add("stoped")
}

function touchedItself() {
    for (let i = 1; i < snake.length; i++) {
        if (snake[0].x == snake[i].x && snake[0].y == snake[i].y) {
            return true;
        }
    }
    return false;
}

function hitBorder() {
    if (snake[0].x < 0 || snake[0].x > width - square) {
        return true;
    }
    if (snake[0].y < 0 || snake[0].y > height - square) {
        return true;
    }
    return false;
}

function changeDirection(d) {
    if (d == "ArrowUp" && direcY != 1) {
        directionY = -1;
        directionX = 0;
    }
    if (d == "ArrowDown" && direcY != -1) {
        directionY = 1;
        directionX = 0;
    }
    if (d == "ArrowLeft" && direcX != 1) {
        directionY = 0;
        directionX = -1;
    }
    if (d == "ArrowRight" && direcX != -1) {
        directionY = 0;
        directionX = 1;
    }
}

function eventListerners() {
    document.addEventListener("keydown", function (event) {
        const keyName = event.key;
        changeDirection(keyName);
    });
    document.getElementById("snake").addEventListener("click", start);
}

function reset() {
    console.log("reset");
    initWindow();
    stopSnake();
    start();
}

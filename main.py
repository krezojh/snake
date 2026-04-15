import pygame      # 게임 화면, 키보드 입력, 도형 그리기 등을 처리하는 라이브러리
import random      # 먹이와 포탈 위치를 무작위로 정하기 위해 사용
import sys         # 프로그램을 완전히 종료하기 위해 사용

# pygame 초기화
pygame.init()

# =========================
# 화면 및 격자 설정
# =========================

CELL_SIZE = 24          # 한 칸의 크기
GRID_WIDTH = 20         # 가로 칸 개수
GRID_HEIGHT = 20        # 세로 칸 개수

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH          # 게임 화면 가로 크기
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + 60   # 상단 정보창 60px 포함한 세로 크기

# 게임 창 생성
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 창 제목 설정
pygame.display.set_caption("Snake Portal Game")

# 게임 속도 조절용 시계 객체
clock = pygame.time.Clock()

# 글자 출력용 폰트
font = pygame.font.SysFont(None, 32)

# =========================
# 색상 설정
# =========================

BLACK = (20, 20, 20)        # 배경색
WHITE = (240, 240, 240)     # 글자색
GREEN = (80, 220, 120)      # 뱀 몸통 색
RED = (240, 80, 80)         # 먹이 색
PURPLE = (160, 90, 255)     # 포탈 색
BLUE = (80, 170, 255)       # 뱀 머리 색
GRAY = (70, 70, 70)         # 게임 영역 테두리 색

# =========================
# 게임 변수
# =========================

snake = [(10, 10)]          # 뱀의 위치 목록, 첫 번째 값이 머리
direction = (1, 0)          # 현재 이동 방향
next_direction = (1, 0)     # 다음 이동 방향

food = (5, 3)               # 먹이 위치
portals = [(3, 3), (16, 16)] # 서로 연결된 포탈 2개 위치

score = 0                   # 현재 점수
high_score = 0              # 최고 점수
food_count = 0              # 먹이를 먹은 횟수

game_state = "start"        # 게임 상태: start, playing, paused, game_over
speed = 7                  # 게임 속도


# =========================
# 글자 출력 함수
# =========================

def draw_text(text, x, y, color=WHITE, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(img, rect)


# =========================
# 빈 칸 무작위 선택 함수
# =========================

def random_empty_cell():
    """
    뱀, 먹이, 포탈과 겹치지 않는 빈 칸을 무작위로 반환하는 함수
    """
    while True:
        pos = (
            random.randint(1, GRID_WIDTH - 2),
            random.randint(1, GRID_HEIGHT - 2)
        )

        # 이미 사용 중인 위치가 아니면 반환
        if pos not in snake and pos != food and pos not in portals:
            return pos


# =========================
# 게임 초기화 함수
# =========================

def reset_game():
    """
    게임을 처음 상태로 되돌리고 바로 시작하는 함수
    """
    global snake, direction, next_direction, food, portals
    global score, food_count, game_state, speed

    snake = [(12, 12)]          # 뱀 위치 초기화
    direction = (1, 0)          # 오른쪽으로 이동 시작
    next_direction = (1, 0)

    score = 0                   # 점수 초기화
    food_count = 0              # 먹이 횟수 초기화
    speed = 7                  # 속도 초기화

    food = random_empty_cell()  # 먹이 위치 새로 생성

    # 포탈 2개 위치 새로 생성
    portals = [random_empty_cell(), random_empty_cell()]

    game_state = "playing"      # 게임 진행 상태로 변경


# =========================
# 화면 그리기 함수
# =========================


def draw_start_page():
    screen.fill(BLACK)

    draw_text("Snake Portal Game", SCREEN_WIDTH // 2, 170, center=True)
    draw_text("Press ENTER to Start", SCREEN_WIDTH // 2, 250, center=True)
    draw_text("Use Arrow Keys or WASD", SCREEN_WIDTH // 2, 300, center=True)
    draw_text("SPACE: Pause / R: Restart / ESC: Quit", SCREEN_WIDTH // 2, 340, center=True)

    pygame.display.flip()


def draw_playing_page():
    screen.fill(BLACK)

    draw_text(f"Score: {score}", SCREEN_WIDTH * 0.15, 30, center=True)
    draw_text(f"High Score: {high_score}", SCREEN_WIDTH * 0.50, 30, center=True)
    draw_text(f"State: {game_state}", SCREEN_WIDTH * 0.85, 30, center=True)

    offset_y = 60

    pygame.draw.rect(
        screen,
        GRAY,
        (0, offset_y, SCREEN_WIDTH, SCREEN_WIDTH),
        2
    )

    fx, fy = food
    pygame.draw.rect(
        screen,
        RED,
        (fx * CELL_SIZE, fy * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
    )

    for px, py in portals:
        pygame.draw.ellipse(
            screen,
            PURPLE,
            (px * CELL_SIZE, py * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
        )

    for i, (x, y) in enumerate(snake):
        color = BLUE if i == 0 else GREEN
        pygame.draw.rect(
            screen,
            color,
            (x * CELL_SIZE, y * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
        )

    pygame.display.flip()


def draw_paused_page():
    draw_playing_page()

    draw_text("Paused", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, center=True)
    draw_text("Press SPACE to Continue", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)

    pygame.display.flip()


def draw_game_over_page():
    screen.fill(BLACK)

    draw_text("Game Over", SCREEN_WIDTH // 2, 170, center=True)
    draw_text(f"Final Score: {score}", SCREEN_WIDTH // 2, 240, center=True)
    draw_text(f"High Score: {high_score}", SCREEN_WIDTH // 2, 285, center=True)
    draw_text("Press R to Restart", SCREEN_WIDTH // 2, 350, center=True)
    draw_text("Press ESC to Quit", SCREEN_WIDTH // 2, 390, center=True)

    pygame.display.flip()


def draw_screen():
    if game_state == "start":
        draw_start_page()
    elif game_state == "playing":
        draw_playing_page()
    elif game_state == "paused":
        draw_paused_page()
    elif game_state == "game_over":
        draw_game_over_page()


# =========================
# 뱀, 먹이, 포탈, 추가로 지정한 위치와 겹치지 않는 빈 칸을 무작위로 반환하는 함수
# =========================

def random_empty_cell(extra_blocked=None):
    
    if extra_blocked is None:
        extra_blocked = []

    while True:
        pos = (
            random.randint(1, GRID_WIDTH - 2),
            random.randint(1, GRID_HEIGHT - 2)
        )

        if (
            pos not in snake
            and pos != food
            and pos not in portals
            and pos not in extra_blocked
        ):
            return pos

# =========================
# 포탈 처리 함수
# =========================

def handle_portal(head):
    """
    뱀의 머리가 포탈에 들어갔는지 확인하는 함수.
    포탈에 들어가면 반대쪽 포탈로 이동하고,
    사용한 뒤 포탈 위치를 새로 바꾼다.
    """
    global score, portals

    if head == portals[0]:
        score += 3
        exit_pos = portals[1]
        portals = [
            random_empty_cell(extra_blocked=[exit_pos]),
            random_empty_cell(extra_blocked=[exit_pos])
        ]
        return exit_pos

    elif head == portals[1]:
        score += 3
        exit_pos = portals[0]
        portals = [
            random_empty_cell(extra_blocked=[exit_pos]),
            random_empty_cell(extra_blocked=[exit_pos])
        ]
        return exit_pos

    return head


# =========================
# 뱀 이동 함수
# =========================

def move_snake():
    """
    뱀을 한 칸 이동시키고 충돌, 먹이, 포탈을 처리하는 함수
    """
    global snake, food, score, food_count, portals
    global game_state, direction, high_score, speed

    # 입력된 다음 방향을 현재 방향으로 적용
    direction = next_direction

    # 현재 머리 위치
    head_x, head_y = snake[0]

    # 이동 방향
    dx, dy = direction

    # 이동 후 머리 위치
    new_head = (head_x + dx, head_y + dy)

    # 포탈에 들어갔는지 확인
    new_head = handle_portal(new_head)

    # 벽 충돌 검사
    if (
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
    ):
        game_state = "game_over"
        high_score = max(high_score, score)
        return

    # 자기 몸 충돌 검사
    if new_head in snake:
        game_state = "game_over"
        high_score = max(high_score, score)
        return

    # 새 머리를 뱀 앞쪽에 추가
    snake.insert(0, new_head)

    # 먹이를 먹은 경우
    if new_head == food:
        score += 10              # 점수 증가
        food_count += 1          # 먹은 먹이 개수 증가

        food = random_empty_cell() # 새 먹이 생성

        # 먹이를 3개 먹을 때마다 포탈 위치 변경
        if food_count % 3 == 0:
            portals = [random_empty_cell(), random_empty_cell()]

        # 먹이를 먹을수록 속도 증가
        speed = min(15, speed + 0.15)

    # 먹이를 먹지 않은 경우
    else:
        snake.pop()              # 꼬리를 제거해 길이 유지


# =========================
# 메인 게임 루프
# =========================

while True:
    # 초당 speed번 반복
    clock.tick(speed)

    # 발생한 이벤트들을 하나씩 확인
    for event in pygame.event.get():

        # 창 닫기 버튼을 누른 경우
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 키보드를 누른 경우
        if event.type == pygame.KEYDOWN:

            # 시작 화면에서 ENTER를 누르면 게임 시작
            if event.key == pygame.K_RETURN and game_state == "start":
                reset_game()

            # SPACE를 누르면 일시정지 또는 재개
            elif event.key == pygame.K_SPACE:
                if game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "playing"

            # R을 누르면 재시작
            elif event.key == pygame.K_r:
                reset_game()

            # ESC를 누르면 종료
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # 게임 진행 중일 때만 방향 전환 가능
            if game_state == "playing":

                # 위쪽 이동
                if event.key in [pygame.K_UP, pygame.K_w] and direction != (0, 1):
                    next_direction = (0, -1)

                # 아래쪽 이동
                elif event.key in [pygame.K_DOWN, pygame.K_s] and direction != (0, -1):
                    next_direction = (0, 1)

                # 왼쪽 이동
                elif event.key in [pygame.K_LEFT, pygame.K_a] and direction != (1, 0):
                    next_direction = (-1, 0)

                # 오른쪽 이동
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and direction != (-1, 0):
                    next_direction = (1, 0)

    # 게임 진행 중일 때만 뱀 이동
    if game_state == "playing":
        move_snake()

    # 매 프레임 화면 다시 그리기
    draw_screen()
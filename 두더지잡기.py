import pygame
import sys
import random
import time


pygame.init()


screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("두더지")
clock = pygame.time.Clock()
FPS = 60


# 시간
start_time = pygame.time.get_ticks()
last_change_time = start_time
game_duration = 60000
# 클릭 무시 시간
click_block_time = 0


# 잡았다! 폰트
catch_font = pygame.font.SysFont("malgungothic", 60)
# 놓쳤다! 폰트
miss_font = pygame.font.SysFont("malgungothic", 60)
# 남은 시간 폰트 (좀 작게)
other_font = pygame.font.SysFont("malgungothic", 30)
# 게임끝 폰트(점수 and 놓친 횟수)
last_font = pygame.font.SysFont("malgungothic", 60)
# 게임끝 폰트(게임이 끝났습니다!)
end_font = pygame.font.SysFont("malgungothic", 90)
# 로비 폰트
game_start_font = pygame.font.SysFont("malgungothic", 60)
# 포획창
message = ""
message_time = 0


# 점수 and 클릭수
score = 0
total_click = 0
miss_mole = 0


# 두더지 구멍
holes = []
hole_size = 100
for row in range(3):
    for col in range(3):
        x = col * hole_size + 50
        y = row * hole_size + 50
        holes.append(pygame.Rect(x, y, hole_size - 20, hole_size - 20))


# 랜덤 위치에 두더지 생성
mole_index = random.randint(0, len(holes) - 1)
mole_click = False

# 게임 상태
game_over = False
# 로비 상태
game_start = False
# 로비 버튼
start_button = pygame.Rect(200, 150, 200, 100)

# 게임 중 실행창
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        # 게임 작동
        if event.type == pygame.QUIT:
            running = False

        # 로비 설정
        if game_start == False and event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                game_start = True
                start_time = pygame.time.get_ticks()
                last_change_time = start_time
                # 0.3초동안 클릭 무시
                click_block_time = start_time + 300

        # 마우스 클릭 감지
        # 두더지 클릭 성공
        if game_start == True and game_over == False and event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() > click_block_time:
            total_click += 1
            if holes[mole_index].collidepoint(event.pos):
                    score += 1
                    mole_click = True
                    message = "잡았다!"
                    message_time = time.time()
                    mole_index = random.randint(0, len(holes) - 1)  # 바로 다음 두더지 등장
                    last_change_time = pygame.time.get_ticks()
                    mole_click = False
            # 엉뚱한 곳 클릭으로 인한 놓침
            else:
                message = "놓쳤다!"
                message_time = time.time()
                mole_index = random.randint(0, len(holes) - 1)
                last_change_time = pygame.time.get_ticks()
                mole_click = False

    # 시간 초과로 인한 놓침 and 1초마다 두더지 위치 바꾸기
    if game_start == True and game_over == False:
        if current_time - last_change_time >= 1000:
            if mole_click == False:  
                miss_mole += 1
                message = "놓쳤다!"
                message_time = time.time()
            mole_index = random.randint(0, len(holes) - 1)
            last_change_time = current_time
            mole_click = False

    # 초록색으로 화면 채우기
    screen.fill((167, 183, 91))

        # 로비창 만들기
    if game_start == False:
        pygame.draw.rect(screen, (0, 100, 0), start_button)
        game_start_text = game_start_font.render("시작", True, (255, 255, 255))
        game_start_rect = game_start_text.get_rect(center=start_button.center)
        screen.blit(game_start_text, game_start_rect)

    elif game_over == False:
        # 60초가 지날 시 게임종료
        if game_over == False and current_time - start_time >= game_duration:
            game_over = True

        # 구멍(녹색) 표현
        for hole in holes:
            pygame.draw.rect(screen, (50, 150, 50), hole)


        # 두더지 생성
        mole_hole = holes[mole_index]
        mole_pos = mole_hole.center
        pygame.draw.circle(screen, (85, 56, 48), mole_pos, hole_size // 3)


        # 잡았다! or 놓쳤다! 표시(0.5초)
        if time.time() - message_time < 0.5:
            if message == "잡았다!":
                text = catch_font.render(message, True, (255, 255, 255))
                text_rect_1 = text.get_rect(center=(465, 320))
                screen.blit(text, text_rect_1)
            elif message =="놓쳤다!":
                text = miss_font.render(message, True, (255, 30, 30))
                text_rect_2 = text.get_rect(center=(465, 320))
                screen.blit(text, text_rect_2)


        # 남은 시간 표시
        remain_time = max(0, game_duration - (current_time - start_time)) // 1000
        timer_text = other_font.render(f"남은 시간: {remain_time}초", True, (255, 255, 255))
        text_rect_3 = timer_text.get_rect(center=(447.5, 60))
        screen.blit(timer_text, text_rect_3)


        # 점수 and 클릭 수 표시
        miss_click = total_click - score
        score_text = other_font.render(f"점수: {score}", True, (255,255,255))
        score_rect = score_text.get_rect(center=(390, 100))
        screen.blit(score_text, score_rect)
        miss_text = other_font.render(f"놓친 횟수: {miss_click + miss_mole}", True, (255, 255 ,255))
        miss_rect = miss_text.get_rect(center=(424.5, 140))
        screen.blit(miss_text, miss_rect)
       
    # 게임 끝났을 때 텍스트 출력
    else:
        screen.fill((50, 50, 50))
        end_text = end_font.render("게임 끝!", True, (255, 255, 255))
        screen.blit(end_text, (140, 10))
        score_text = last_font.render(f"점수: {score}", True, (255,255,255))
        screen.blit(score_text, (120, 145))
        miss_text = last_font.render(f"놓친 횟수: {miss_click + miss_mole}", True, (255, 255 ,255))
        screen.blit(miss_text, (120, 230))


    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()
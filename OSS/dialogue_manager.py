import sys
import pygame
import time

class DialogueManager:
    def __init__(self, screen, font, text_color=(255, 255, 255), box_color=(20, 20, 50)):
        self.screen = screen
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        
        # 대화창 위치 및 크기
        self.box_rect = pygame.Rect(50, screen.get_height() - 180, screen.get_width() - 60, 180)
        self.text_start_pos = (self.box_rect.left + 20, self.box_rect.top + 20)
        
        self.full_text = ""
        self.lines = []
        self.line_height = self.font.get_height() + 5
        
        self.char_per_sec = 40  # 초당 40글자 출력
        self.current_char_count = 0.0
        self.finished = False
        self.is_displaying = False

    def set_text(self, text):
        """표시할 텍스트와 타이핑 애니메이션을 초기화합니다."""
        self.full_text = text
        self.current_char_count = 0.0
        self.finished = False
        self.is_displaying = True
        
        # 텍스트를 대화창 폭에 맞춰 여러 줄로
        self.lines = self._wrap_text(text)
        
    def _wrap_text(self, text):
        """텍스트를 대화창 폭에 맞게 줄 바꿈 처리합니다."""
        max_width = self.box_rect.width - 40 # 패딩
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            # 현재 줄에 단어를 추가했을 때의 너비를 확인
            test_line = current_line + " " + word if current_line else word
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def update(self):
        """텍스트 애니메이션 업데이트"""
        if not self.is_displaying or self.finished:
            return

        # 글자 수 증가
        self.current_char_count += self.char_per_sec * (1 / 30.0) # 30FPS
        
        if self.current_char_count >= len(self.full_text):
            self.current_char_count = len(self.full_text)
            self.finished = True
    
    def draw(self):
        """대화창과 텍스트 화면 그리기 """
        if not self.is_displaying:
            return
            
        # 1. 배경 박스 그리기
        pygame.draw.rect(self.screen, self.box_color, self.box_rect, border_radius=10) #배경색
        pygame.draw.rect(self.screen, (255, 255, 255), self.box_rect, 3, border_radius=10) # 테두리

        # 2. 텍스트 출력
        total_chars_drawn = 0
        y_pos = self.text_start_pos[1]
        
        for line in self.lines:
            chars_to_draw = int(self.current_char_count) - total_chars_drawn
            if chars_to_draw <= 0:
                break
            
            # 현재 줄에서 출력할 부분만 잘라냄
            segment_to_render = line[:chars_to_draw]
            text_surface = self.font.render(segment_to_render, True, self.text_color)
            self.screen.blit(text_surface, (self.text_start_pos[0], y_pos))
            
            total_chars_drawn += len(line)
            y_pos += self.line_height
            
            if total_chars_drawn > self.current_char_count:
                break # 현재 줄에서 타이핑이 끝나야 함
                
    def wait_for_input(self):
        """텍스트 출력이 완료될 때까지, 또는 사용자가 키를 누를 때까지 대기하고 즉시 종료"""
        
        if not hasattr(self, 'clock'):
            self.clock = pygame.time.Clock()

        while self.is_displaying:
            self.update()
            self.draw()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    if not self.finished:
                        # 텍스트가 아직 출력 중이면, 즉시 전체 텍스트를 표시
                        self.current_char_count = len(self.full_text)
                        self.finished = True
                    else:
                        # 전체 텍스트 표시가 완료되었으면, 대화창 닫기
                        self.is_displaying = False
                        
                        #핵심 수정: 이벤트 큐를 비워 다음 단계 지연 해결
                        pygame.event.clear() 
                        
                        return # 메인 스토리로 즉시 복귀
            
            self.clock.tick(30)
import pygame
import pandas as pd
import sys

# --- VISUAL THEME & COLORS ---
COLOR_BG = (30, 32, 38)          # Dark Charcoal
COLOR_PANEL = (40, 44, 52)       # Slate Gray
COLOR_ROBOT = (0, 210, 255)      # Cyan Neon
COLOR_INBOUND = (152, 195, 121)  # Soft Green
COLOR_TEXT = (220, 223, 228)     # Off White
COLOR_ACCENT = (198, 120, 221)   # Purple Accent


SHELF_COLORS = {
    "Electronics": (224, 108, 117),    # Soft Red
    "Furniture": (229, 192, 123),      # Soft Yellow
    "Food and Drink": (97, 175, 239),  # Soft Blue
    "Consumables": (86, 182, 194),     # Teal
    "Damaged items": (144, 144, 154)   # Slate Gray (New!)
}

# --- DIMENSIONS ---
WIDTH, HEIGHT = 1200, 850  # Tăng chiều cao một chút để đủ chỗ 5 kệ
INBOUND_POS = (150, 400)
SHELF_X = 950


SHELF_MAP = {
    "Electronics": 100,
    "Furniture": 240,
    "Food and Drink": 380,
    "Consumables": 520,
    "Damaged items": 660  # Vị trí kệ mới
}

class AutonomousRobot:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        self.speed = 7
        self.payload = None
        self.state = "NAV_TO_PICKUP" 

    def update(self):
        move_vec = self.target - self.pos
        if move_vec.length() > self.speed:
            self.pos += move_vec.normalize() * self.speed
            return False
        else:
            self.pos = pygame.Vector2(self.target)
            return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smart Logistics AI Simulator v2.5")
    clock = pygame.time.Clock()
    
    # Fonts
    font_main = pygame.font.SysFont("Segoe UI", 24, bold=True)
    font_sub = pygame.font.SysFont("Segoe UI", 18)
    font_ui = pygame.font.SysFont("Consolas", 16)

    # Load Data
    try:
        df = pd.read_csv('load.csv', encoding='utf-8-sig')
        # Loại bỏ khoảng trắng thừa trong tên cột nếu có
        df.columns = df.columns.str.strip()
        mission_list = df.to_dict('records')
    except Exception as e:
        print(f"Error loading load.csv: {e}")
        return

    robot = AutonomousRobot(50, 50)
    task_idx = 0
    logs = ["System Initialized...", "Waiting for load.csv commands..."]
    is_finished = False

    while True:
        screen.fill(COLOR_BG)
        
        # 1. DRAW WAREHOUSE FLOOR (GRID)
        for x in range(0, WIDTH, 50):
            pygame.draw.line(screen, (45, 45, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(screen, (45, 45, 50), (0, y), (WIDTH, y))

        # 2. DRAW DASHBOARD (UI PANEL)
        pygame.draw.rect(screen, COLOR_PANEL, (0, 0, WIDTH, 80))
        pygame.draw.line(screen, COLOR_ACCENT, (0, 80), (WIDTH, 80), 3)
        screen.blit(font_main.render("SMART WAREHOUSE CONTROL CENTER", True, COLOR_ACCENT), (20, 15))
        
        # Progress Bar
        total_tasks = len(mission_list)
        progress = (task_idx / total_tasks) * 300
        pygame.draw.rect(screen, (60, 60, 70), (WIDTH - 350, 30, 300, 20), border_radius=5)
        pygame.draw.rect(screen, COLOR_INBOUND, (WIDTH - 350, 30, progress, 20), border_radius=5)
        screen.blit(font_ui.render(f"Efficiency: {int((task_idx/total_tasks)*100)}%", True, COLOR_TEXT), (WIDTH - 350, 55))

        # 3. DRAW INBOUND AREA
        pygame.draw.rect(screen, COLOR_INBOUND, (100, 350, 100, 100), 2, border_radius=10)
        screen.blit(font_sub.render("INBOUND", True, COLOR_INBOUND), (110, 320))

        # 4. DRAW SHELVES
        for cat, y_pos in SHELF_MAP.items():
            color = SHELF_COLORS.get(cat, COLOR_TEXT)
            # Vẽ bóng đổ cho kệ
            pygame.draw.rect(screen, (20, 20, 25), (SHELF_X + 5, y_pos + 5, 220, 80), border_radius=8)
            # Vẽ kệ chính
            pygame.draw.rect(screen, color, (SHELF_X, y_pos, 220, 80), border_radius=8)
            pygame.draw.rect(screen, COLOR_PANEL, (SHELF_X + 5, y_pos + 5, 210, 70), border_radius=5)
            screen.blit(font_sub.render(cat, True, color), (SHELF_X + 15, y_pos + 25))

        # 5. ROBOT AI LOGIC
        if not is_finished:
            current_item = mission_list[task_idx]
            
            if robot.state == "NAV_TO_PICKUP":
                robot.target = pygame.Vector2(INBOUND_POS)
                if robot.update():
                   
                    robot.payload = current_item.get('ItemName', 'Unknown')
                    logs.append(f"Picked up: {robot.payload}")
                    
                   
                    category = current_item.get('Category', 'Consumables')
                    target_y = SHELF_MAP.get(category, 400)
                    robot.target = pygame.Vector2(SHELF_X, target_y + 40)
                    robot.state = "NAV_TO_SHELF"
            
            elif robot.state == "NAV_TO_SHELF":
                if robot.update():
                    logs.append(f"Stored {robot.payload} in {current_item.get('Category')} Shelf")
                    robot.payload = None
                    task_idx += 1
                    if task_idx >= total_tasks:
                        is_finished = True
                        robot.target = pygame.Vector2(100, 100) # Go home
                    else:
                        robot.state = "NAV_TO_PICKUP"
        else:
            robot.update()
            complete_txt = font_main.render("ALL LOGISTICS MISSIONS COMPLETED", True, COLOR_INBOUND)
            screen.blit(complete_txt, (WIDTH//2 - 200, HEIGHT//2))

        # 6. DRAW ROBOT
        # Glow Effect
        pygame.draw.circle(screen, (30, 80, 100), (int(robot.pos.x), int(robot.pos.y)), 35)
        pygame.draw.circle(screen, COLOR_ROBOT, (int(robot.pos.x), int(robot.pos.y)), 25)
        pygame.draw.circle(screen, COLOR_TEXT, (int(robot.pos.x), int(robot.pos.y)), 25, 3)
        
        if robot.payload:
            # Vẽ kiện hàng trên lưng robot
            pygame.draw.rect(screen, (209, 154, 102), (robot.pos.x - 15, robot.pos.y - 15, 30, 30), border_radius=3)
            label = font_ui.render(robot.payload, True, COLOR_TEXT)
            screen.blit(label, (robot.pos.x - 40, robot.pos.y - 45))

        # 7. LOG WINDOW (Bottom Left)
        pygame.draw.rect(screen, (20, 22, 26), (20, HEIGHT - 180, 450, 160), border_radius=10)
        pygame.draw.rect(screen, COLOR_ACCENT, (20, HEIGHT - 180, 450, 160), 1, border_radius=10)
        for i, log in enumerate(logs[-6:]): 
            screen.blit(font_ui.render(f"> {log}", True, (171, 178, 191)), (35, HEIGHT - 165 + i*22))

        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
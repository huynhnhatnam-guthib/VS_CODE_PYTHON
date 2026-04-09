import pygame
import pandas as pd
import sys
import math

#  CONFIGURATION & COLORS 
COLORS = {
    "bg": (12, 14, 18),
    "grid": (25, 28, 35),
    "panel": (32, 35, 45),
    "accent": (0, 255, 220),
    "sorter": (255, 60, 60),
    "deliverer": (255, 215, 0),
    "inbound": (50, 255, 100),
    "gate": (180, 70, 255),
    "shelf_frame": (60, 65, 80),
    "money": (255, 215, 0),
    "text": (220, 225, 230),
    "bay_wall": (50, 55, 70)
}

WIDTH, HEIGHT = 1600, 800 
POS_INBOUND = (150, 220) 
POS_GATE = (150, 500)     
SHELF_X = 1250 
POS_REST_SORTER = (500, 675)   
POS_REST_DELIVERER = (720, 675) 
STATION_X, STATION_Y = 420, 600

SHELF_MAP = {
    "Electronics": 100, "Furniture": 215, "Food and Drink": 330,
    "Consumables": 445, "Damaged items": 560 
}

class Robot:
    def __init__(self, x, y, color, speed, name):
        self.pos = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        self.speed = speed
        self.color = color
        self.name = name
        self.payload = None
        self.state = "RESTING"
        self.angle = 0

    def move(self):
        distance = self.target - self.pos
        if distance.length() > self.speed:
            desired_angle = math.degrees(math.atan2(-distance.y, distance.x))
            self.angle += (desired_angle - self.angle) * 0.1
            self.pos += distance.normalize() * self.speed
            return False
        self.pos = pygame.Vector2(self.target)
        return True

    def draw(self, screen, font):
        glow_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color, 40), (40, 40), 35)
        screen.blit(glow_surf, (self.pos.x - 40, self.pos.y - 40))
        pts = []
        for i in range(6):
            a = math.radians(self.angle + i * 60)
            pts.append((self.pos.x + 25 * math.cos(a), self.pos.y - 25 * math.sin(a)))
        pygame.draw.polygon(screen, self.color, pts)
        pygame.draw.polygon(screen, (255, 255, 255), pts, 2)
        eye_x = self.pos.x + 12 * math.cos(math.radians(self.angle))
        eye_y = self.pos.y - 12 * math.sin(math.radians(self.angle))
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), 5)
        if self.payload:
            lbl = font.render(str(self.payload), True, (255, 255, 255))
            screen.blit(lbl, (self.pos.x - 40, self.pos.y - 65))

def draw_shelf(screen, x, y, title, font, count):
    pygame.draw.rect(screen, COLORS["shelf_frame"], (x, y, 320, 95), 4, border_radius=5)
    for i in range(16):
        row, col = i // 8, i % 8
        box_x, box_y = x + 10 + col * 38, y + 8 if row == 0 else y + 55
        color = (255, 140, 0) if i < count else (25, 28, 35)
        pygame.draw.rect(screen, color, (box_x, box_y, 30, 25), border_radius=3)
        pygame.draw.rect(screen, COLORS["shelf_frame"], (box_x, box_y, 30, 25), 1, border_radius=3)
    screen.blit(font.render(title, True, COLORS["accent"]), (x + 5, y - 22))

def draw_status_box(screen, font, x, y, robot, color):
    pygame.draw.rect(screen, (15, 17, 22), (x, y, 180, 45), border_radius=8)
    pygame.draw.rect(screen, color, (x, y, 180, 45), 1, border_radius=8)
    screen.blit(font.render(f"{robot.name}: {robot.state}", True, color), (x + 10, y + 12))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CYBER-LOGISTICS v17.0 - OPERATION")
    clock = pygame.time.Clock()
    f_main = pygame.font.SysFont("Agency FB", 45, bold=True)
    f_ui = pygame.font.SysFont("Calibri", 18, bold=True)

    try:
        df = pd.read_csv('load.csv', encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        pending_items = df.to_dict('records')
        work_order = []
        system_running = False
    except Exception as e: print(f"Error: {e}"); return

    sorter = Robot(POS_REST_SORTER[0], POS_REST_SORTER[1], COLORS["sorter"], 7, "SORTER")
    deliverer = Robot(POS_REST_DELIVERER[0], POS_REST_DELIVERER[1], COLORS["deliverer"], 10, "DELIVERY")
    
    ship_idx, revenue = 0, 0
    ready_to_ship, logs = [], ["> STANDBY: CHOOSE ORDER"]
    inventory_counts = {cat: 0 for cat in SHELF_MAP}
    shipping_queue = []

    while True:
        screen.fill(COLORS["bg"])
        
        #  MÀN HÌNH 1: CHỌN THỨ TỰ (PLANNER) 
        if not system_running:
            screen.blit(f_main.render("PLANNING MODE: SELECT SEQUENCE", True, COLORS["accent"]), (WIDTH//2 - 250, 40))
            
            pygame.draw.rect(screen, (30, 32, 40), (100, 120, 600, 550), border_radius=15)
            screen.blit(f_ui.render("AVAILABLE ITEMS (Click to pick):", True, COLORS["inbound"]), (120, 140))
            
            item_btns = []
            for i, item in enumerate(pending_items[:15]): 
                row, col = i % 5, i // 5
                btn_rect = pygame.Rect(120 + col * 200, 180 + row * 80, 180, 60)
                pygame.draw.rect(screen, (50, 55, 70), btn_rect, border_radius=8)
                screen.blit(f_ui.render(item['ItemName'][:15], True, (255, 255, 255)), (btn_rect.x + 10, btn_rect.y + 10))
                screen.blit(f_ui.render(f"({item['Category']})", True, (150, 150, 150)), (btn_rect.x + 10, btn_rect.y + 35))
                item_btns.append((btn_rect, item))

            pygame.draw.rect(screen, (20, 22, 28), (850, 120, 600, 550), border_radius=15)
            pygame.draw.rect(screen, COLORS["accent"], (850, 120, 600, 550), 2, border_radius=15)
            screen.blit(f_ui.render("CURRENT PLAN:", True, COLORS["sorter"]), (870, 140))
            
            for i, item in enumerate(work_order):
                y_pos = 180 + i * 25
                if y_pos < 650:
                    screen.blit(f_ui.render(f"{i+1}. {item['ItemName']} -> {item['Category']}", True, (220, 220, 220)), (870, y_pos))

            start_btn_rect = pygame.Rect(WIDTH//2 - 150, 700, 300, 70)
            if len(work_order) > 0:
                pygame.draw.rect(screen, (0, 200, 120), start_btn_rect, border_radius=15)
                screen.blit(f_main.render("START SYSTEM", True, (255, 255, 255)), (WIDTH//2 - 100, 710))

        #  MÀN HÌNH 2: VẬN HÀNH (EXECUTION) 
        else:
            for x in range(0, WIDTH, 60):
                for y in range(0, HEIGHT, 60):
                    pygame.draw.rect(screen, COLORS["grid"], (x, y, 60, 60), 1)

            pygame.draw.rect(screen, (20, 22, 28), (0, 0, WIDTH, 80))
            pygame.draw.line(screen, COLORS["accent"], (0, 80), (WIDTH, 80), 3)
            screen.blit(f_main.render("CYBER-LOGISTICS OPERATIONAL SYSTEM", True, COLORS["accent"]), (40, 18))
            screen.blit(f_main.render(f"BANK: ${revenue:,.0f}", True, COLORS["money"]), (WIDTH - 350, 18))

            pygame.draw.rect(screen, COLORS["inbound"], (POS_INBOUND[0]-70, POS_INBOUND[1]-70, 140, 140), 3, border_radius=15)
            screen.blit(f_ui.render("INBOUND", True, COLORS["inbound"]), (POS_INBOUND[0]-40, POS_INBOUND[1]-95))
            pygame.draw.rect(screen, COLORS["gate"], (POS_GATE[0]-70, POS_GATE[1]-70, 140, 140), 3, border_radius=15)
            screen.blit(f_ui.render("DELIVERY", True, COLORS["gate"]), (POS_GATE[0]-40, POS_GATE[1]-95))
            
            for cat, y_pos in SHELF_MAP.items():
                draw_shelf(screen, SHELF_X, y_pos, cat, f_ui, inventory_counts[cat])

            # Charging Station & Walls
            pygame.draw.rect(screen, (30, 35, 45), (STATION_X, STATION_Y, 450, 180), border_radius=20)
            pygame.draw.rect(screen, COLORS["accent"], (STATION_X, STATION_Y, 450, 180), 2, border_radius=20)
            for wall_x in [450, 550, 670, 770]:
                pygame.draw.rect(screen, COLORS["bay_wall"], (wall_x, 625, 10, 100))
            screen.blit(f_ui.render("ROBOT CHARGING STATION", True, COLORS["accent"]), (STATION_X + 20, STATION_Y + 10))
            
            # Khôi phục Bảng Trạng thái Robot
            draw_status_box(screen, f_ui, 455, 725, sorter, COLORS["sorter"])
            draw_status_box(screen, f_ui, 675, 725, deliverer, COLORS["deliverer"])

            # Khôi phục Log Panel
            log_rect = pygame.Rect(WIDTH - 380, 680, 360, 100)
            pygame.draw.rect(screen, (10, 10, 15), log_rect, border_radius=15)
            pygame.draw.rect(screen, COLORS["accent"], log_rect, 1, border_radius=15)
            for i, log in enumerate(logs[-4:]):
                screen.blit(f_ui.render(log, True, (150, 160, 170)), (WIDTH - 365, 690 + i*20))

            #  Sorter Logic 
            if len(work_order) > 0 or sorter.payload:
                if sorter.state in ["IDLE", "RESTING"] and len(work_order) > 0:
                    sorter.state = "NAV_PICKUP"
                if sorter.state == "NAV_PICKUP":
                    sorter.target = pygame.Vector2(POS_INBOUND)
                    if sorter.move():
                        sorter.payload = work_order[0]['ItemName']
                        sorter.target = pygame.Vector2(SHELF_X - 50, SHELF_MAP[work_order[0]['Category']] + 47)
                        sorter.state = "NAV_SHELF"
                elif sorter.state == "NAV_SHELF":
                    if sorter.move():
                        inventory_counts[work_order[0]['Category']] += 1
                        logs.append(f"> STORED: {sorter.payload}") 
                        if work_order[0]['Category'] != "Damaged items":
                            shipping_queue.append(work_order[0])
                        sorter.payload = None
                        work_order.pop(0)
                        sorter.state = "IDLE"
            else:
                sorter.target = pygame.Vector2(POS_REST_SORTER)
                if sorter.move(): sorter.state = "RESTING"

            #  Deliverer Logic 
            if ship_idx < len(shipping_queue):
                ship_item = shipping_queue[ship_idx]
                if deliverer.state in ["IDLE", "RESTING"]: deliverer.state = "NAV_SHELF"
                if deliverer.state == "NAV_SHELF":
                    deliverer.target = pygame.Vector2(SHELF_X - 50, SHELF_MAP[ship_item['Category']] + 47)
                    if deliverer.move():
                        deliverer.payload = ship_item['ItemName']
                        inventory_counts[ship_item['Category']] -= 1
                        deliverer.target = pygame.Vector2(POS_GATE)
                        deliverer.state = "NAV_GATE"
                elif deliverer.state == "NAV_GATE":
                    if deliverer.move():
                        revenue += ship_item['Price']
                        logs.append(f"> SHIPPED: {deliverer.payload}") 
                        deliverer.payload = f"CASH: ${ship_item['Price']}"
                        deliverer.target = pygame.Vector2(POS_GATE); deliverer.state = "DEPOSIT"
                elif deliverer.state == "DEPOSIT":
                    if deliverer.move():
                        deliverer.payload = None; ship_idx += 1; deliverer.state = "NAV_SHELF"
            else:
                deliverer.target = pygame.Vector2(POS_REST_DELIVERER)
                if deliverer.move(): deliverer.state = "RESTING"

            sorter.draw(screen, f_ui)
            deliverer.draw(screen, f_ui)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not system_running:
                    for btn, item in item_btns:
                        if btn.collidepoint(event.pos):
                            work_order.append(item)
                            pending_items.remove(item)
                    if len(work_order) > 0 and start_btn_rect.collidepoint(event.pos):
                        system_running = True
                        logs.append("> SYSTEM STARTED. EXECUTING PLAN.")

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
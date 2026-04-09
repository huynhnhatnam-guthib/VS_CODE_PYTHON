import pygame
import pandas as pd
import sys
import math
import random

# --- CONFIGURATION & COLORS ---
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

# --- 1. PYGAME THẤP LẠI (NGANG CHUẨN) ---
WIDTH, HEIGHT = 1600, 800 

POS_INBOUND = (150, 220) 
POS_GATE = (150, 500)    
SHELF_X = 1250 

# --- 2. TỌA ĐỘ NGHỈ (KHỚP VỚI HỘC SẠC) ---
POS_REST_SORTER = (500, 675)   
POS_REST_DELIVERER = (720, 675) 

# Căn chỉnh kệ hàng để không bị bảng Log che
SHELF_MAP = {
    "Electronics": 100, 
    "Furniture": 215, 
    "Food and Drink": 330,
    "Consumables": 445, 
    "Damaged items": 560  # Kết thúc tại Y=660
}

class Robot:
    def __init__(self, x, y, color, speed, name):
        self.pos = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        self.speed = speed
        self.color = color
        self.name = name
        self.payload = None
        self.state = "IDLE"
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

def draw_shelf(screen, x, y, title, font):
    pygame.draw.rect(screen, COLORS["shelf_frame"], (x, y, 320, 95), 4, border_radius=5)
    pygame.draw.line(screen, COLORS["shelf_frame"], (x, y + 47), (x + 320, y + 47), 2)
    for i in range(8):
        box_x = x + 10 + i * 38
        pygame.draw.rect(screen, (random.randint(150, 200), 100, 50), (box_x, y + 8, 30, 25))
        pygame.draw.rect(screen, (100, 120, 150), (box_x, y + 55, 30, 25))
    screen.blit(font.render(title, True, COLORS["accent"]), (x + 5, y - 22))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CYBER-LOGISTICS ULTRA-WIDE v14.5")
    clock = pygame.time.Clock()
    f_main = pygame.font.SysFont("Agency FB", 40, bold=True)
    f_ui = pygame.font.SysFont("Calibri", 17, bold=True)

    try:
        df = pd.read_csv('load.csv', encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        all_items = df.to_dict('records')
        shipping_list = [i for i in all_items if i['Category'] != "Damaged items"]
    except Exception as e:
        print(f"Error: {e}"); return

    sorter = Robot(POS_REST_SORTER[0], POS_REST_SORTER[1], COLORS["sorter"], 7, "SORTER")
    deliverer = Robot(POS_REST_DELIVERER[0], POS_REST_DELIVERER[1], COLORS["deliverer"], 10, "DELIVERY")
    
    sort_idx, ship_idx, revenue = 0, 0, 0
    ready_to_ship, logs = [], ["> SYSTEM WIDENED", "> ENCLOSED BAYS ACTIVE"]

    while True:
        screen.fill(COLORS["bg"])
        for x in range(0, WIDTH, 60):
            for y in range(0, HEIGHT, 60):
                pygame.draw.rect(screen, COLORS["grid"], (x, y, 60, 60), 1)

        # 1. HEADER
        pygame.draw.rect(screen, (20, 22, 28), (0, 0, WIDTH, 80))
        pygame.draw.line(screen, COLORS["accent"], (0, 80), (WIDTH, 80), 3)
        screen.blit(f_main.render("CYBER-WAREHOUSE LOGISTICS PRO", True, COLORS["accent"]), (40, 18))
        screen.blit(f_main.render(f"BANK: ${revenue:,.0f}", True, COLORS["money"]), (WIDTH - 350, 18))

        # 2. ZONES (BÊN TRÁI)
        pygame.draw.rect(screen, COLORS["inbound"], (POS_INBOUND[0]-70, POS_INBOUND[1]-70, 140, 140), 3, border_radius=15)
        screen.blit(f_ui.render("INBOUND", True, COLORS["inbound"]), (POS_INBOUND[0]-40, POS_INBOUND[1]-95))
        pygame.draw.rect(screen, COLORS["gate"], (POS_GATE[0]-70, POS_GATE[1]-70, 140, 140), 3, border_radius=15)
        screen.blit(f_ui.render("DELIVERY", True, COLORS["gate"]), (POS_GATE[0]-40, POS_GATE[1]-95))

        # 3. SHELVES (BÊN PHẢI)
        for cat, y_pos in SHELF_MAP.items():
            draw_shelf(screen, SHELF_X, y_pos, cat, f_ui)

        # 4. ENCLOSED CHARGING STATION (LAYER 1 - NỀN)
        station_x, station_y = 420, 600
        pygame.draw.rect(screen, (30, 35, 45), (station_x, station_y, 450, 180), border_radius=20)
        pygame.draw.rect(screen, (20, 20, 25), (460, 635, 80, 80), border_radius=10) # Slot 1
        pygame.draw.rect(screen, (20, 20, 25), (680, 635, 80, 80), border_radius=10) # Slot 2

        # 5. ROBOTS (VẼ GIỮA CÁC LỚP TRẠM SẠC)
        # Logic di chuyển
        if sort_idx < len(all_items):
            current = all_items[sort_idx]
            if sorter.state in ["IDLE", "RESTING"]: sorter.state = "NAV_PICKUP"
            if sorter.state == "NAV_PICKUP":
                sorter.target = pygame.Vector2(POS_INBOUND)
                if sorter.move():
                    sorter.payload = current['ItemName']
                    sorter.target = pygame.Vector2(SHELF_X - 50, SHELF_MAP[current['Category']] + 47)
                    sorter.state = "NAV_SHELF"
            elif sorter.state == "NAV_SHELF":
                if sorter.move():
                    logs.append(f"> STORED: {sorter.payload}")
                    if current['Category'] != "Damaged items": ready_to_ship.append(current['ItemID'])
                    sorter.payload = None; sort_idx += 1; sorter.state = "NAV_PICKUP"
        else:
            sorter.target = pygame.Vector2(POS_REST_SORTER)
            if sorter.move(): sorter.state = "RESTING"

        if ship_idx < len(shipping_list):
            ship_item = shipping_list[ship_idx]
            if ship_item['ItemID'] in ready_to_ship:
                if deliverer.state in ["IDLE", "RESTING"]: deliverer.state = "NAV_SHELF"
                if deliverer.state == "NAV_SHELF":
                    deliverer.target = pygame.Vector2(SHELF_X - 50, SHELF_MAP[ship_item['Category']] + 47)
                    if deliverer.move():
                        deliverer.payload = ship_item['ItemName']
                        deliverer.target = pygame.Vector2(POS_GATE)
                        deliverer.state = "NAV_GATE"
                elif deliverer.state == "NAV_GATE":
                    if deliverer.move():
                        revenue += ship_item['Price']; logs.append(f"> SHIPPED: {deliverer.payload}")
                        deliverer.payload = f"CASH: ${ship_item['Price']}"
                        deliverer.target = pygame.Vector2(WIDTH//2, 40); deliverer.state = "DEPOSIT"
                elif deliverer.state == "DEPOSIT":
                    if deliverer.move():
                        deliverer.payload = None; ship_idx += 1; deliverer.state = "NAV_SHELF"
            else:
                deliverer.target = pygame.Vector2(POS_REST_DELIVERER)
                if deliverer.move(): deliverer.state = "RESTING"
        else:
            deliverer.target = pygame.Vector2(POS_REST_DELIVERER)
            if deliverer.move(): deliverer.state = "RESTING"

        sorter.draw(screen, f_ui)
        deliverer.draw(screen, f_ui)

        # 6. CHARGING STATION (LAYER 2 - VÁCH NGĂN & CHỮ)
        # Vách ngăn cơ khí che một phần robot
        pygame.draw.rect(screen, COLORS["bay_wall"], (450, 625, 10, 100))
        pygame.draw.rect(screen, COLORS["bay_wall"], (550, 625, 10, 100))
        pygame.draw.rect(screen, COLORS["bay_wall"], (670, 625, 10, 100))
        pygame.draw.rect(screen, COLORS["bay_wall"], (770, 625, 10, 100))
        pygame.draw.rect(screen, COLORS["accent"], (station_x, station_y, 450, 180), 2, border_radius=20)
        screen.blit(f_ui.render("ROBOT CHARGING STATION", True, COLORS["accent"]), (station_x + 20, station_y + 10))
        
        # Bảng trạng thái robot đẩy xuống dưới hộc sạc
        def draw_status_box(x, y, robot, color):
            pygame.draw.rect(screen, (15, 17, 22), (x, y, 180, 45), border_radius=8)
            pygame.draw.rect(screen, color, (x, y, 180, 45), 1, border_radius=8)
            screen.blit(f_ui.render(f"{robot.name}: {robot.state}", True, color), (x + 10, y + 12))

        draw_status_box(455, 725, sorter, COLORS["sorter"])
        draw_status_box(675, 725, deliverer, COLORS["deliverer"])

        # 7. LOG PANEL (BÊN PHẢI DƯỚI)
        log_rect = pygame.Rect(WIDTH - 380, 680, 360, 100)
        pygame.draw.rect(screen, (10, 10, 15), log_rect, border_radius=15)
        pygame.draw.rect(screen, COLORS["accent"], log_rect, 1, border_radius=15)
        for i, log in enumerate(logs[-4:]):
            screen.blit(f_ui.render(log, True, (150, 160, 170)), (WIDTH - 365, 690 + i*20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        pygame.display.flip(); clock.tick(60)

if __name__ == "__main__":
    main()
import pygame
import pandas as pd
import sys
import time

# --- GRAPHICS SETUP ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AUTOMATED GOODS SORTING ROBOT")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# Colors
WHITE = (255, 255, 255)
ROBOT_COLOR = (255, 0, 0)
SHELF_COLOR = (70, 70, 70)
INBOUND_POS = (100, 300)

# Automated shelf coordinates by category
SHELF_LOCATIONS = {
    "Electronics": (800, 50),
    "Monitors": (800, 140),
    "Kitchenware": (800, 230),
    "Dried Food": (800, 320),
    "Beverages": (800, 410),
    "Adhesives": (800, 500)
}

# --- ROBOT CLASS ---
class Robot:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        self.speed = 7
        self.carrying = None
        self.state = "GET_TASK" # GET_TASK -> TO_INBOUND -> TO_SHELF

def run_simulation():
    # Read load.csv file
    try:
        # Note: Ensure your CSV headers are 'ItemName' and 'Category'
        df = pd.read_csv('load.csv', encoding='utf-8-sig')
        tasks = df.to_dict('records')
    except:
        print("❌ File 'load.csv' is required to run!")
        return

    robot = Robot(INBOUND_POS[0], INBOUND_POS[1])
    task_index = 0
    done = False

    while True:
        screen.fill(WHITE)
        
        # Draw loading station and shelves
        pygame.draw.rect(screen, (0, 200, 0), (50, 250, 100, 100), 2)
        for cat, pos in SHELF_LOCATIONS.items():
            pygame.draw.rect(screen, SHELF_COLOR, (pos[0], pos[1], 160, 60))
            screen.blit(font.render(cat, True, WHITE), (pos[0] + 5, pos[1] + 20))

        # AUTOMATIC LOGIC (No manual input required)
        if task_index < len(tasks):
            current_task = tasks[task_index]
            
            if robot.state == "GET_TASK":
                robot.target = pygame.Vector2(INBOUND_POS)
                if (robot.target - robot.pos).length() < 5:
                    robot.carrying = current_task['ItemName']
                    # Default to middle of screen if category is not found
                    dest = SHELF_LOCATIONS.get(current_task['Category'], (500, 300))
                    robot.target = pygame.Vector2(dest)
                    robot.state = "TO_SHELF"
            
            elif robot.state == "TO_SHELF":
                if (robot.target - robot.pos).length() < 5:
                    print(f"📦 Successfully stored: {current_task['ItemName']}")
                    robot.carrying = None
                    task_index += 1
                    robot.state = "GET_TASK"
        else:
            done = True
            robot.target = pygame.Vector2(50, 50) # Return to home/rest station

        # Robot Movement logic
        if (robot.target - robot.pos).length() > 0:
            move_vec = (robot.target - robot.pos).normalize() * robot.speed
            robot.pos += move_vec

        # Draw Robot
        pygame.draw.circle(screen, ROBOT_COLOR, (int(robot.pos.x), int(robot.pos.y)), 20)
        if robot.carrying:
            screen.blit(font.render(robot.carrying, True, (200, 0, 0)), (robot.pos.x - 20, robot.pos.y - 40))

        if done:
            screen.blit(font.render("ALL ITEMS PROCESSED!", True, (0, 150, 0)), (400, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_simulation()
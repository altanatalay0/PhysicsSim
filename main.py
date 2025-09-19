import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Physics Simulation")

space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

clock = pygame.time.Clock()
FPS = 60

static_lines = [
    pymunk.Segment(space.static_body, (0, 0), (800, 0), 5),
    pymunk.Segment(space.static_body, (0, 600), (800, 600), 5),
    pymunk.Segment(space.static_body, (0, 0), (0, 600), 5),
    pymunk.Segment(space.static_body, (800, 0), (800, 600), 5)
]
for line in static_lines:
    line.elasticity = 0.8
    space.add(line)

font = pygame.font.SysFont("Arial", 20)

tabs = {
    "ADD": {"open": False, "items": ["Circle", "Square"]},
    "PLANET": {"open": False, "items": [{"Earth": (0, 900)}, {"Mars": (0, 300)}]}
}

selected_item = None

def draw_menu():
    x, y = 10, 10
    for tab_name, tab_data in tabs.items():
        pygame.draw.rect(screen, (50, 50, 200), (x, y, 100, 30))
        text = font.render(tab_name, True, (255, 255, 255))
        screen.blit(text, (x + 10, y + 5))

        if tab_data["open"]:
            for i, item in enumerate(tab_data["items"]):
                display_name = str(list(item.keys())[0]) if isinstance(item, dict) else item
                color = (100, 200, 100) if item == selected_item else (100, 100, 250)
                pygame.draw.rect(screen, color, (x, y + 35 + i*35, 100, 30))
                text = font.render(display_name, True, (255, 255, 255))
                screen.blit(text, (x + 10, y + 40 + i*35))
        y += 120

def check_menu_click(pos):
    global selected_item
    x, y = 10, 10
    for tab_name, tab_data in tabs.items():
        main_rect = pygame.Rect(x, y, 100, 30)
        if main_rect.collidepoint(pos):
            tab_data["open"] = True
            return True
        if tab_data["open"]:
            for i, item in enumerate(tab_data["items"]):
                item_rect = pygame.Rect(x, y + 35 + i*35, 100, 30)
                if item_rect.collidepoint(pos):
                    selected_item = item
                    return True
        y += 120
    return False

def add_circle(space, position):
    mass = 1
    radius = 30
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8
    space.add(body, shape)

def add_square(space, position):
    mass = 1
    size = 40
    moment = pymunk.moment_for_box(mass, (size, size))
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly.create_box(body, (size, size))
    shape.elasticity = 0.8
    space.add(body, shape)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not check_menu_click(event.pos):
                if selected_item == "Circle":
                    add_circle(space, event.pos)
                elif selected_item == "Square":
                    add_square(space, event.pos)
                elif isinstance(selected_item, dict):
                    for planet in selected_item:
                        space.gravity = selected_item[planet]

    screen.fill((0,0,0))
    space.step(1/FPS)
    space.debug_draw(draw_options)
    draw_menu()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

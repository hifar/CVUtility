import pygame
import math
from pygame.locals import *

# 初始化PyGame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("RGB Cube")
clock = pygame.time.Clock()

# 立方体参数
cube_size = 255
step = 10  # 调整此值以改变颜色过渡的平滑度

# 创建立方体的各个面
faces = []

# 前面 (z=255)
for x in range(0, cube_size, step):
    for y in range(0, cube_size, step):
        x_end = min(x + step, cube_size)
        y_end = min(y + step, cube_size)
        points = [
            (x, y, cube_size),
            (x_end, y, cube_size),
            (x_end, y_end, cube_size),
            (x, y_end, cube_size),
        ]
        cx = (x + x_end) // 2
        cy = (y + y_end) // 2
        color = (cx, cy, cube_size)
        faces.append({'points': points, 'color': color})

# 后面 (z=0)
for x in range(0, cube_size, step):
    for y in range(0, cube_size, step):
        x_end = min(x + step, cube_size)
        y_end = min(y + step, cube_size)
        points = [
            (x, y, 0),
            (x_end, y, 0),
            (x_end, y_end, 0),
            (x, y_end, 0),
        ]
        cx = (x + x_end) // 2
        cy = (y + y_end) // 2
        color = (cx, cy, 0)
        faces.append({'points': points, 'color': color})

# 右面 (x=255)
for y in range(0, cube_size, step):
    for z in range(0, cube_size, step):
        y_end = min(y + step, cube_size)
        z_end = min(z + step, cube_size)
        points = [
            (cube_size, y, z),
            (cube_size, y, z_end),
            (cube_size, y_end, z_end),
            (cube_size, y_end, z),
        ]
        cy = (y + y_end) // 2
        cz = (z + z_end) // 2
        color = (cube_size, cy, cz)
        faces.append({'points': points, 'color': color})

# 左面 (x=0)
for y in range(0, cube_size, step):
    for z in range(0, cube_size, step):
        y_end = min(y + step, cube_size)
        z_end = min(z + step, cube_size)
        points = [
            (0, y, z),
            (0, y, z_end),
            (0, y_end, z_end),
            (0, y_end, z),
        ]
        cy = (y + y_end) // 2
        cz = (z + z_end) // 2
        color = (0, cy, cz)
        faces.append({'points': points, 'color': color})

# 上面 (y=255)
for x in range(0, cube_size, step):
    for z in range(0, cube_size, step):
        x_end = min(x + step, cube_size)
        z_end = min(z + step, cube_size)
        points = [
            (x, cube_size, z),
            (x_end, cube_size, z),
            (x_end, cube_size, z_end),
            (x, cube_size, z_end),
        ]
        cx = (x + x_end) // 2
        cz = (z + z_end) // 2
        color = (cx, cube_size, cz)
        faces.append({'points': points, 'color': color})

# 下面 (y=0)
for x in range(0, cube_size, step):
    for z in range(0, cube_size, step):
        x_end = min(x + step, cube_size)
        z_end = min(z + step, cube_size)
        points = [
            (x, 0, z),
            (x_end, 0, z),
            (x_end, 0, z_end),
            (x, 0, z_end),
        ]
        cx = (x + x_end) // 2
        cz = (z + z_end) // 2
        color = (cx, 0, cz)
        faces.append({'points': points, 'color': color})

# 旋转参数
rotate_x = 0
rotate_y = 0
dragging = False
last_mouse_pos = (0, 0)
scale = 0.5  # 缩放因子，使立方体适应屏幕

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                last_mouse_pos = event.pos
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == MOUSEMOTION and dragging:
            current_mouse_pos = event.pos
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            rotate_y += dx * 0.01
            rotate_x += dy * 0.01
            last_mouse_pos = current_mouse_pos

    screen.fill((0, 0, 0))

    # 计算旋转矩阵
    cos_y = math.cos(rotate_y)
    sin_y = math.sin(rotate_y)
    cos_x = math.cos(rotate_x)
    sin_x = math.sin(rotate_x)

    rotation_matrix = [
        [cos_y, sin_y * sin_x, sin_y * cos_x],
        [0, cos_x, -sin_x],
        [-sin_y, cos_y * sin_x, cos_y * cos_x]
    ]

    # 投影所有面并排序
    projected_faces = []
    for face in faces:
        rotated_points = []
        z_coords = []
        for (x, y, z) in face['points']:
            # 平移到立方体中心
            xc = x - 127.5
            yc = y - 127.5
            zc = z - 127.5

            # 应用旋转矩阵
            xr = xc * rotation_matrix[0][0] + yc * rotation_matrix[0][1] + zc * rotation_matrix[0][2]
            yr = xc * rotation_matrix[1][0] + yc * rotation_matrix[1][1] + zc * rotation_matrix[1][2]
            zr = xc * rotation_matrix[2][0] + yc * rotation_matrix[2][1] + zc * rotation_matrix[2][2]

            # 平移回原位置并投影
            screen_x = int(xr * scale) + width // 2
            screen_y = int(yr * scale) + height // 2
            rotated_points.append((screen_x, screen_y))
            z_coords.append(zr)

        # 计算平均深度
        avg_z = sum(z_coords) / len(z_coords)
        projected_faces.append((avg_z, rotated_points, face['color']))

    # 按深度从远到近排序
    projected_faces.sort(key=lambda x: -x[0])

    # 绘制所有面
    for z, points, color in projected_faces:
        pygame.draw.polygon(screen, color, points)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
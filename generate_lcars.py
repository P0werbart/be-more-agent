import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1280
HEIGHT = 720
BG_COLOR = (0, 0, 0)

# TNG Authentic LCARS Colors
PEACH = (255, 153, 102)
ORANGE = (255, 153, 0)
LAVENDER = (204, 153, 255)
LIGHT_BLUE = (153, 204, 255)
PINK = (255, 102, 153)
RED = (204, 0, 0)
YELLOW = (255, 204, 0)

def get_base_colors(state):
    if state == "error": return RED, RED, RED, YELLOW
    if state == "warmup": return YELLOW, PEACH, ORANGE, LAVENDER
    return PEACH, ORANGE, LAVENDER, LIGHT_BLUE

def draw_lcars_elbow(draw, state):
    c1, c2, c3, c4 = get_base_colors(state)
    
    # Left main Elbow
    # Outer rectangle
    draw.rounded_rectangle([40, 40, 400, HEIGHT - 40], radius=40, fill=c1)
    # Inner cut-out to make the elbow shape (this cuts out the center leaving the L shape)
    draw.rounded_rectangle([180, 120, 1280, HEIGHT - 100], radius=40, fill=BG_COLOR)
    # Ensure the right side of the inner cut-out is completely flat so the bottom bar extends
    draw.rectangle([180, 120, 1280, HEIGHT - 100], fill=BG_COLOR)
    # Re-draw the inner round corner specifically
    draw.rounded_rectangle([180, 120, 300, 240], radius=40, fill=BG_COLOR)
    
    # Right side blocks (Top bar extension)
    draw.rounded_rectangle([420, 40, 700, 100], radius=30, fill=c2)
    draw.rounded_rectangle([720, 40, 1000, 100], radius=30, fill=c3)
    draw.rounded_rectangle([1020, 40, 1240, 100], radius=30, fill=c4)
    
    # Right side blocks (Bottom bar extension)
    draw.rounded_rectangle([420, HEIGHT - 80, 600, HEIGHT - 40], radius=20, fill=c2)
    draw.rounded_rectangle([620, HEIGHT - 80, 900, HEIGHT - 40], radius=20, fill=c3)
    draw.rounded_rectangle([920, HEIGHT - 80, 1240, HEIGHT - 40], radius=20, fill=c1)
    
    # Left sidebar split blocks (cutting the elbow)
    # We cut the elbow with black lines
    draw.rectangle([40, 160, 180, 170], fill=BG_COLOR)
    draw.rectangle([40, 240, 180, 250], fill=BG_COLOR)
    draw.rectangle([40, 320, 180, 330], fill=BG_COLOR)
    draw.rectangle([40, 500, 180, 510], fill=BG_COLOR)
    
    # Fill the cut parts with different colors
    draw.rectangle([40, 170, 180, 240], fill=c3)
    draw.rectangle([40, 250, 180, 320], fill=c4)
    draw.rectangle([40, 510, 180, HEIGHT - 100], fill=c2)
    
    # Bottom Left corner rounding fix
    draw.rounded_rectangle([40, HEIGHT - 100, 180, HEIGHT - 40], radius=40, fill=c1)
    draw.rectangle([40, HEIGHT - 100, 180, HEIGHT - 60], fill=c1)

def draw_data_blocks(draw, state):
    c1, c2, c3, c4 = get_base_colors(state)
    colors = [c1, c2, c3, c4, PINK]
    
    try:
        import platform
        if platform.system() == "Windows":
            font = ImageFont.truetype("arialbd.ttf", 20)
            font_title = ImageFont.truetype("arialbd.ttf", 34)
            font_small = ImageFont.truetype("arial.ttf", 16)
        else:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
            font_small = ImageFont.truetype("DejaVuSans.ttf", 16)
    except:
        font = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Title Texts (Black on Colored Bars)
    draw.text((200, 55), "AUDIO ANALYSIS", fill=BG_COLOR, font=font_title)
    draw.text((800, 55), "SYSTEM", fill=BG_COLOR, font=font_title)
    draw.text((1060, 55), "STATUS", fill=BG_COLOR, font=font_title)
    
    # Top Right Grid Data (Dense numbers)
    random.seed(42) # Consistent random numbers
    for row in range(5):
        for col in range(3):
            x = 950 + col * 90
            y = 150 + row * 25
            val = f"{random.randint(10, 999)}.{random.randint(1,9)}"
            draw.text((x, y), val, fill=random.choice(colors), font=font)
            
    # Small decorative graph top left
    for i in range(15):
        h = random.randint(5, 30)
        draw.rectangle([220 + i*15, 180 - h, 230 + i*15, 180], fill=c4)
        
    # Bottom Right Data
    for row in range(4):
        x = 950
        y = 480 + row * 30
        draw.rectangle([x, y+5, x+40, y+15], fill=random.choice(colors))
        draw.text((x + 50, y), f"SEC {random.randint(1000, 9999)}", fill=c2, font=font)

    # Some textual lines
    for i in range(5):
        y = 520 + i * 20
        draw.text((220, y), f"PARAMETER {i+1}   ...................................   {random.randint(10,99)}%", fill=c3, font=font_small)

def draw_waveform_mirrored(draw, state, frame=0):
    c1, c2, c3, c4 = get_base_colors(state)
    colors = [c1, c2, c3, c4, PINK]
    
    center_y = 340
    start_x = 220
    end_x = 900
    bar_width = 6
    spacing = 4
    
    num_bars = (end_x - start_x) // (bar_width + spacing)
    
    for i in range(num_bars):
        x = start_x + i * (bar_width + spacing)
        
        color = colors[i % len(colors)]
        if state == "error": color = RED
            
        if state == "idle":
            amp = 5
        elif state == "listening":
            amp = 15 + 10 * math.sin(i * 0.2 + frame * 0.8)
        elif state == "thinking":
            amp = 50 if (i - frame*2) % 12 < 6 else 5
        elif state == "speaking":
            # Very complex high-res wave
            base = 120 * math.sin(i * 0.3 + frame * 1.5)
            high = 80 * math.sin(i * 1.1 - frame * 2.1)
            mid = 50 * math.sin(i * 0.7 + frame * 0.5)
            envelope = math.sin(math.pi * i / num_bars)
            amp = abs(base + high + mid) * envelope + 10
        elif state == "warmup":
            progress = frame / 5.0
            if i / num_bars < progress:
                amp = 80 * math.sin(i * 0.5) + 20
            else:
                amp = 5
        elif state == "error":
            amp = 80 if (i + frame) % 2 == 0 else 5
        else:
            amp = 5
            
        amp = max(2, min(160, amp))
        
        # Draw top and bottom parts of the wave with a gap in the middle
        draw.rectangle([x, center_y - amp, x + bar_width, center_y - 2], fill=color)
        draw.rectangle([x, center_y + 2, x + bar_width, center_y + amp], fill=color)

def generate_state(state, num_frames):
    out_dir = f"faces_computer/{state}"
    os.makedirs(out_dir, exist_ok=True)
    
    for f in os.listdir(out_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(out_dir, f))
            
    for f in range(num_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        draw_lcars_elbow(draw, state)
        draw_data_blocks(draw, state)
        draw_waveform_mirrored(draw, state, f)
        
        img.save(os.path.join(out_dir, f"{f+1}.png"))
        print(f"Generated {state} frame {f+1}")

if __name__ == "__main__":
    generate_state("idle", 1)
    generate_state("listening", 10)
    generate_state("thinking", 10)
    generate_state("speaking", 15)
    generate_state("error", 2)
    generate_state("warmup", 6)
    print("All enhanced LCARS BOOM images generated successfully.")

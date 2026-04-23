# pip install Pillow

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

def create_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
    draw.pieslice([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=fill)
    draw.pieslice([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=fill)
    draw.pieslice([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=fill)
    draw.pieslice([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=fill)

def generate_frames():
    output_base = "faces_computer"
    states = ["idle", "listening", "thinking", "speaking", "error", "warmup", "capturing"]
    
    for state in states:
        os.makedirs(os.path.join(output_base, state), exist_ok=True)
        
    width, height = 1280, 720
    
    # Try to load a font, fallback to default
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_med = ImageFont.truetype("arial.ttf", 30)
        font_small = ImageFont.truetype("arial.ttf", 16)
        font_warmup = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font_large = font_med = font_small = font_warmup = ImageFont.load_default()
        
    for frame in range(1, 7):
        # --- IDLE ---
        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        
        # Sidebar Base Logic
        def draw_layout(draw, sidebar_color, frame_num, top_color, is_idle=False):
            # Top bar
            draw.rectangle([0, 0, width, 20], fill=top_color)
            # Bottom bar
            draw.rectangle([0, height-12, width, height], fill="#9999FF") # Blue
            
            # Left sidebar
            gap = 8
            w = 80
            y = 40
            h1, h2, h3 = 60, 120, 60
            
            c1 = c2 = c3 = sidebar_color
            if is_idle:
                shade_shift = "#CC7700" if frame_num % 3 == 0 else sidebar_color
                if frame_num % 3 == 0: c1 = shade_shift
                elif frame_num % 3 == 1: c2 = shade_shift
                else: c3 = shade_shift
                
            create_rounded_rect(draw, [20, y, 20+w, y+h1], 15, fill=c1)
            y += h1 + gap
            create_rounded_rect(draw, [20, y, 20+w, y+h2], 15, fill=c2)
            y += h2 + gap
            create_rounded_rect(draw, [20, y, 20+w, y+h3], 15, fill=c3)
            
            # Stardate
            draw.text((width - 200, 30), "STARDATE 2401.15", fill="white", font=font_small)
            
        # IDLE Frame
        draw_layout(draw, "#FF9900", frame, "#FF9900", is_idle=True)
        draw.text((400, 300), "LCARS ONLINE", fill="#9999FF", font=font_large)
        draw.text((400, 380), "AWAITING INPUT", fill="#FF9900", font=font_small)
        img.save(os.path.join(output_base, "idle", f"frame_{frame:03d}.png"))
        
        # --- LISTENING ---
        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        draw_layout(draw, "#FF9900", frame, "#FF9900")
        draw.text((350, 300), "VOICE INPUT ACTIVE", fill="#FF9900", font=font_large)
        
        # Waveform bars
        bar_w = 40
        bar_gap = 20
        start_x = 450
        y_base = 450
        for i in range(4):
            bar_h = random.randint(20, 100)
            draw.rectangle([start_x, y_base-bar_h, start_x+bar_w, y_base], fill="#FF9900")
            start_x += bar_w + bar_gap
        img.save(os.path.join(output_base, "listening", f"frame_{frame:03d}.png"))

        # --- THINKING ---
        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        # Background Grid
        grid_alpha = 50 + (frame % 3) * 50
        for gx in range(200, width, 50):
            for gy in range(50, height, 50):
                draw.rectangle([gx, gy, gx+4, gy+4], fill=(grid_alpha, grid_alpha, grid_alpha))
                
        draw_layout(draw, "#CC88FF", frame, "#CC88FF")
        draw.text((400, 300), "PROCESSING", fill="#CC88FF", font=font_large)
        
        dots = ["◆ ◇ ◇", "◇ ◆ ◇", "◇ ◇ ◆"]
        draw.text((400, 380), dots[frame % 3], fill="#CC88FF", font=font_med)
        img.save(os.path.join(output_base, "thinking", f"frame_{frame:03d}.png"))
        
        # --- SPEAKING ---
        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        draw_layout(draw, "#44FF88", frame, "#44FF88")
        draw.text((380, 200), "VOCAL OUTPUT", fill="#44FF88", font=font_large)
        
        # Spectrum visualizer
        start_x = 380
        y_base = 500
        for i in range(12):
            bar_h = random.randint(10, 150)
            draw.rectangle([start_x, y_base-bar_h, start_x+20, y_base], fill="#44FF88")
            start_x += 30
        img.save(os.path.join(output_base, "speaking", f"frame_{frame:03d}.png"))

        # --- ERROR ---
        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        # Diagonal warning stripes
        for sx in range(-height, width, 100):
            draw.line([(sx, 0), (sx+height, height)], fill="#440000", width=30)
            
        draw_layout(draw, "#FF4444", frame, "#FF4444")
        
        if frame % 2 == 0:
            draw.text((400, 300), "SYSTEM ALERT", fill="#FF4444", font=font_large)
        else:
            draw.text((400, 300), "SYSTEM ALERT", fill="#880000", font=font_large)
        img.save(os.path.join(output_base, "error", f"frame_{frame:03d}.png"))
        
        # --- CAPTURING ---
        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        draw_layout(draw, "#33CCFF", frame, "#33CCFF")
        draw.text((350, 200), "VISUAL SENSOR ACTIVE", fill="#33CCFF", font=font_large)
        
        # Rotating Crosshair
        cx, cy = 600, 450
        r = 100
        angle = frame * 15
        import math
        for a in [0, 90, 180, 270]:
            rad = math.radians(a + angle)
            x1 = cx + int(math.cos(rad) * (r-20))
            y1 = cy + int(math.sin(rad) * (r-20))
            x2 = cx + int(math.cos(rad) * (r+20))
            y2 = cy + int(math.sin(rad) * (r+20))
            draw.line([(x1, y1), (x2, y2)], fill="#33CCFF", width=5)
        draw.arc([cx-r, cy-r, cx+r, cy+r], 0, 360, fill="#33CCFF", width=2)
        img.save(os.path.join(output_base, "capturing", f"frame_{frame:03d}.png"))
        
        # --- WARMUP ---
        img = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(img)
        draw_layout(draw, "#FF9900", frame, "#FF9900")
        
        lines = [
            "LCARS BOOT SEQUENCE INITIATED",
            "LOADING NEURAL MATRIX...",
            "VOICE RECOGNITION ONLINE",
            "LANGUAGE MODEL CONNECTED",
            "ALL SYSTEMS NOMINAL",
            "COMPUTER READY"
        ]
        
        y_text = 200
        for i in range(frame):
            color = "#FF9900" if i == 5 else "#9999FF"
            draw.text((300, y_text), lines[i], fill=color, font=font_warmup)
            y_text += 40
            
        img.save(os.path.join(output_base, "warmup", f"frame_{frame:03d}.png"))

    print("LCARS frame generation complete.")
    print(f"Generated 6 frames each for states: {', '.join(states)}")
    print(f"Output directory: {output_base}")

if __name__ == '__main__':
    generate_frames()

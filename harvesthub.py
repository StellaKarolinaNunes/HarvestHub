import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
from io import BytesIO

def create_gradient(width, height, stops):
    img = Image.new("RGBA", (width, height))
    for y in range(height):
        pos = y / (height - 1)
        for i in range(len(stops) - 1):
            p0, c0, a0 = stops[i]
            p1, c1, a1 = stops[i+1]
            if p0 <= pos <= p1:
                f = (pos - p0) / (p1 - p0) if p1-p0 != 0 else 0
                rgb0 = tuple(int(c0[i:i+2], 16) for i in (1, 3, 5))
                rgb1 = tuple(int(c1[i:i+2], 16) for i in (1, 3, 5))
                rgb = tuple(int(rgb0[j] + (rgb1[j] - rgb0[j]) * f) for j in range(3))
                alpha = int(a0 + (a1 - a0) * f)
                for x in range(width):
                    img.putpixel((x, y), (*rgb, alpha))
                break
    return img

def create_rounded_rectangle_image(width, height, radius, border_width, border_color, fill_color):
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [0, 0, width, height],
        radius=radius,
        fill=border_color
    )
    draw.rounded_rectangle(
        [border_width, border_width, width-border_width, height-border_width],
        radius=radius - border_width,
        fill=fill_color
    )
    return img

def get_github_icon(size):
    # Fallback: baixar PNG do GitHub logo
    icon_url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    response = requests.get(icon_url)
    icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    icon_img = icon_img.resize((size, size), Image.LANCZOS)
    return icon_img

def main():
    stops = [
        (0.0, "#FFB6B9", 255),
        (0.5, "#FDCDC9", 128),
        (0.75, "#B5EAD7", 255),
        (1.0, "#C7CEEA", 255),
    ]
    WIDTH, HEIGHT = 650, 500

    root = tk.Tk()
    root.title("HarvestHub")
    root.resizable(False, False)
    root.geometry(f"{WIDTH}x{HEIGHT}")

    gradient_img = create_gradient(WIDTH, HEIGHT, stops)
    gradient_tk = ImageTk.PhotoImage(gradient_img)
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=gradient_tk)

    rect_w, rect_h = 420, 357
    rect_radius = 22
    border_width = 2.5
    border_color = "#000000"
    fill_color = "#FFFFFF"

    rect_img = create_rounded_rectangle_image(
        rect_w, rect_h, rect_radius, border_width, border_color, fill_color
    )
    rect_tk = ImageTk.PhotoImage(rect_img)
    x = (WIDTH - rect_w)//2
    y = (HEIGHT - rect_h)//2
    canvas.create_image(x, y, anchor="nw", image=rect_tk)

    # Icone GitHub centralizado no topo do retângulo
    icon_size = 64
    github_icon_img = get_github_icon(icon_size)
    github_icon_tk = ImageTk.PhotoImage(github_icon_img)
    icon_x = x + rect_w//2
    icon_y = y + 22//2 + 12  # margem do topo arredondado
    canvas.create_image(icon_x, icon_y, anchor="n", image=github_icon_tk)

    # Texto abaixo do logo
    title_text = "HarvestHub - Github Downloader"
    font_family = "JetBrains Mono"
    font_size = 16

    # Tentar usar JetBrains Mono, senão fallback
    try:
        from tkinter import font as tkfont
        # Pode ser necessário instalar JetBrains Mono no sistema
        title_font = tkfont.Font(family=font_family, size=font_size)
    except Exception:
        title_font = ("Arial", font_size, "bold")

    # Calcula posição do texto: logo + margem (~12px)
    text_y = icon_y + icon_size + 10
    canvas.create_text(
        icon_x, text_y,
        text=title_text,
        font=title_font,
        fill="#222",
        anchor="n"
    )

    canvas.gradient_img = gradient_tk
    canvas.rect_img = rect_tk
    canvas.github_icon_img = github_icon_tk

    root.mainloop()

if __name__ == "__main__":
    main()
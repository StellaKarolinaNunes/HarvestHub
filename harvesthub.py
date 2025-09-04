import tkinter as tk
from PIL import Image, ImageTk

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

def main():
    stops = [
        (0.0, "#FFB6B9", 255),
        (0.5, "#FDCDC9", 128),
        (0.75, "#B5EAD7", 255),
        (1.0, "#C7CEEA", 255),
    ]
    WIDTH, HEIGHT = 650, 500

    root = tk.Tk()
    root.title("harvesthub")
    root.resizable(False, False)
    root.geometry(f"{WIDTH}x{HEIGHT}")

    gradient_img = create_gradient(WIDTH, HEIGHT, stops)
    gradient_tk = ImageTk.PhotoImage(gradient_img)
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=gradient_tk)

    root.mainloop()

if __name__ == "__main__":
    main()

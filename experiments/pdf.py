"""
generates 3000 compressed pdfs with random ascii text and fonts.
its just here to pad the existing pdf dataset
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import random
import string
import os

OUTPUT_DIR = "dataset/pdf"
COUNT = 3000

os.makedirs(OUTPUT_DIR, exist_ok=True)

FONTS = ["Helvetica", "Times-Roman", "Courier", "Helvetica-Bold", "Times-Italic"]
PAGE_SIZES = [letter, A4]

def random_text(min_words=20, max_words=300):
    words = []
    for _ in range(random.randint(min_words, max_words)):
        word_len = random.randint(2, 10)
        words.append(''.join(random.choices(string.ascii_lowercase, k=word_len)))
    return ' '.join(words)

for i in range(COUNT):
    path = os.path.join(OUTPUT_DIR, f"doc_{i}.pdf")
    c = canvas.Canvas(path, pagesize=random.choice(PAGE_SIZES))

    num_pages = random.randint(1, 8)
    for page in range(num_pages):
        font = random.choice(FONTS)
        size = random.randint(8, 18)
        c.setFont(font, size)

        y = 750
        text = random_text()
        words = text.split()
        line = ""
        for word in words:
            if len(line) + len(word) > 80:
                c.drawString(50, y, line)
                y -= size + 4
                line = word
                if y < 50:
                    break
            else:
                line += " " + word
        if line:
            c.drawString(50, y, line)

        c.showPage()
    
    c.setPageCompression(1)

    c.save()

    if i % 500 == 0:
        print(f"{i}/{COUNT}")

print("done")
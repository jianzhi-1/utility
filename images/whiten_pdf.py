import argparse
import fitz  # pymupdf
import os
from PIL import Image
import tempfile

def clean_background(img, threshold=600):
    img = img.convert("RGB")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            if r + g + b > threshold:
                pixels[x, y] = (255, 255, 255)
            # if min(r, g, b) > 100 and r > 100:
            #     pixels[x, y] = (255, 255, 255)
    return img

def process_pdf(input_pdf_path, output_pdf_path, threshold=600, zoom=4):
    with tempfile.TemporaryDirectory() as temp_dir:
        doc = fitz.open(input_pdf_path)
        cleaned_images = []

        for i, page in enumerate(doc):
          
            # render page to image
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_path = os.path.join(temp_dir, f"page_{i}.png")
            pix.save(img_path)

            pil_img = Image.open(img_path)
            cleaned_img = clean_background(pil_img, threshold)
            cleaned_images.append(cleaned_img)

        cleaned_images[0].save(output_pdf_path, "PDF", resolution=100.0, save_all=True, append_images=cleaned_images[1:])

    print(f"PDF saved to: {output_pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output", type=str, default="output.pdf")
    parser.add_argument("-t", "--threshold", type=int, default=500)
    parser.add_argument("-z", "--zoom", type=int, default=4)
    args = parser.parse_args()

    input_pdf = f"./{args.filename}"
    output_pdf = f"./{args.output}"

    threshold = args.threshold
    zoom = args.zoom

    process_pdf(input_pdf, output_pdf, threshold=threshold, zoom=zoom)

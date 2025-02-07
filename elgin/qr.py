import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont


def generate_codebar(number, codigo):
    index = len(str(number))

    codigo = codigo[:-index] + str(number)
    barcode_class = barcode.get_barcode_class("code128")

    
    meu_codigo_bar = barcode_class(codigo, writer=ImageWriter())

    meu_codigo_bar.save("Teste", options={"write_text": False})

    img = Image.open("Teste.png")

    largura, altura = img.size

    nova_largura = largura + 250
    nova_img = Image.new("RGB", (nova_largura, altura), "white")

    nova_img.paste(img, (0, 0))

    draw = ImageDraw.Draw(nova_img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 45)
    except IOError:
        font = ImageFont.load_default()
    

    bbox = draw.textbbox((0, 0), number, font=font)
    text_largura = bbox[2] - bbox[0]
    text_altura = bbox[3] - bbox[1]

    text_x = largura + 70
    text_y = (altura - text_altura) // 2  # Centraliza verticalmente o texto ao lado do código de barras

    draw.text((text_x, text_y), number, font=font, fill="black")

    nova_img.save(r"C:\Users\User\Desktop\your-directory\codigo_barra.png")

    print("Código de barras gerado e salvo como: codigo_barra.png")





# generate_codebar("18000", "9788512354679")
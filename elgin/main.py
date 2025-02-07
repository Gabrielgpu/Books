import os
import win32print
import win32ui
from PIL import Image, ImageWin

class PrintHandler:
    def __init__(self, printer_name, max_width=700, max_height=700):
        self.printer_name = printer_name
        self.max_width = max_width
        self.max_height = max_height

    def print_image(self, image_path):
        img = Image.open(image_path)

        img.thumbnail((self.max_width, self.max_height))

        if img.mode != 'RGB':
            img = img.convert('RGB')

        elgin = win32print.OpenPrinter(self.printer_name)
        try:
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(self.printer_name)

            hdc.StartDoc(image_path)
            hdc.StartPage()

            page_width = hdc.GetDeviceCaps(110)
            page_height = hdc.GetDeviceCaps(111)

            x = (page_width - img.size[0]) // 2
            y = (page_height - img.size[1]) // 2


            dib = ImageWin.Dib(img)
            dib.draw(hdc.GetHandleOutput(), (x, y, x + img.size[0], y + img.size[1]))

            hdc.EndPage()
            hdc.EndDoc()

            hdc.DeleteDC()

            print(f"Imagem {image_path} enviada para a impressora {self.printer_name} com sucesso.")
        
        except Exception as e:
            print(f"Erro ao imprimir: {e}")
            hdc.AbortDoc()
        finally:
            win32print.ClosePrinter(elgin)

    def search_and_print(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                image_path = os.path.join(directory, filename)
                print(f"Arquivo PNG encontrado: {image_path}")
                self.print_image(image_path)

                try:
                    os.remove(image_path)
                    print(f"Arquivo {image_path} excluído após a impressão.")
                
                except OSError as e:
                    print(f"Erro ao excluir o arquivo {image_path}: {e}")


if __name__ == "__main__":
    directory_to_search = r"C:\Users\User\Desktop\your-directory"
    printer_name = "ELGIN L42PRO FULL"
    handler = PrintHandler(printer_name)
    handler.search_and_print(directory_to_search)

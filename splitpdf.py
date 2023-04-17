import fitz
from typing import Tuple
from time import time
import os
from PIL import Image
import configparser

def convert_pdf2img(input_file: str, pages: Tuple = None):
    """Преобразует PDF в изображение и создает файл за страницей"""
    pdfIn = fitz.open(input_file)
    output_files = []
    try:
        zoom_x,zoom_y = int(settings['DEFAULT']['zoom']),int(settings['DEFAULT']['zoom'])
        crop_width, crop_height = int(settings[str(zoom_x)]['crop_width']), int(settings[str(zoom_x)]['crop_height'])
        shift_x = int(settings[str(zoom_x)]['shift_x']) 
        shift_y = int(settings[str(zoom_x)]['shift_y'])
    except:
        zoom_x,zoom_y = 1, 1
        crop_width = 98
        crop_height = 169
        shift_x = 5
        shift_y = 5
    for pg in range(pdfIn.page_count):
        if str(pages) != str(None):
            if str(pg) not in str(pages):
                continue
        page = pdfIn[pg]
        rotate = int(0)
        # PDF Страница конвертируется в целое изображение 1056 * 816, а затем для каждого изображения делается снимок экрана.
        # zoom = 1.33333333 -----> Размер изображения = 1056 * 816
        # zoom = 2 ---> 2 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = маленький размер файла/размер изображения = 1584 * 1224
        # zoom = 4 ---> 4 * Разрешение по умолчанию (текст четкий, текст изображения плохо читается) = большой размер файла
        # zoom = 8 ---> 8 * Разрешение по умолчанию (текст четкий, текст изображения читается) = большой размер файла
        # Коэффициент масштабирования 8, чтобы текст был четким   
        
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom_x, zoom_y), alpha=False)
        output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}_page{pg+1}.png"
        pix.save(output_file)
        img = Image.open(output_file)
        for i in range(4):
            for j in range(5):
                cr_left = (crop_width+shift_x)*j
                cr_top = (crop_height+shift_y)*i
                cr_right = cr_left + crop_width
                cr_bottom = cr_top + crop_height
                output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}_page{pg+1}_pic"+str(i+1)+str(j+1)+".png"
                img.crop((cr_left, cr_top, cr_right, cr_bottom)).save(output_file, quality=100)
                #img.show()
                output_files.append(output_file)
        
    pdfIn.close()
    summary = {
                "Исходный файл":  input_file,    "Изображений": str(len(output_files)), "Выходной файл(ы)": str(output_files)
            }           
            # Printing Summary
    print("#### Отчет ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return output_files
  

if __name__ == "__main__":
    import sys
    start = time()
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
    try:
        input_file = sys.argv[1]
    except:
        input_file = 'e:\\test.pdf'
    convert_pdf2img(input_file)
    print("Время работы: ",int(time()-start),"секунд")
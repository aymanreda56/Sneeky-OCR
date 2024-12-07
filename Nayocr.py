import easyocr
import PIL, os, sys
from ar_corrector.corrector import Corrector

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(base_path, "model")

if os.path.exists(model_path) and not os.path.isdir(model_path):
    raise ValueError(f"Path {model_path} exists but is not a directory!")

def ocr(PIL_img_obj):

    PIL_img_obj.save('temp.png')
    reader = easyocr.Reader(lang_list=['ar'], gpu=False, model_storage_directory=model_path, download_enabled=False)

    output = reader.readtext(image='temp.png', paragraph=True, height_ths=3, x_ths=2, y_ths=0.3)
    img = PIL_img_obj

    drawer = PIL.ImageDraw.Draw(img, mode='RGBA')

    result_str = """"""
    for res in output:
        result_str += res[-1]
        result_str += "\n"
        drawer.rectangle((tuple(res[0][0]) , tuple(res[0][2])), outline = 'Red', width = 2)
    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write(result_str)

    img.save('test_detected.png', 'PNG')
    return result_str, img, output


# correcting all typos
def correct(output_obj:list, text:str=None):
    corr = Corrector()
    corrected_text = """"""

    if(not text):
        for res in output_obj:
            par = corr.contextual_correct(res[-1])
            corrected_text += par
            corrected_text += "\n"
    else:
        corrected_text = corr.contextual_correct(text)
        
    with open ('resultscorrected.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n\n\n')
        f.write(corrected_text)
    
    return corrected_text



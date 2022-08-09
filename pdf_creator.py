import os
from docx import Document
from datetime import datetime
from docx2pdf import convert
import aspose.words as aw

def concat(dir, final):
    bar = '/'
    bar += final
    dir += bar
    return dir

def salvar_PDF(directory, serial, client_name, employee_name, color, problem):
    now = datetime.now()
    datetimetoday = now.strftime("%d_%m_%Y %H_%M_%S")

    list = ['{employee}', '{client}', '{serial_number}', '{color}', '{problem}']
    list2 = [employee_name, client_name, serial, color, problem]

    doc = aw.Document("C:/Users/vinic/Downloads/OEG-20220729T223604Z-001/OEG/formulario_template.docx")

    for i in range(0, 5):
        doc.range.replace(list[i], list2[i], aw.replacing.FindReplaceOptions(aw.replacing.FindReplaceDirection.FORWARD))

    file_name = "{0} {1}.pdf".format(serial, datetimetoday)
    directory = concat(directory, file_name)
    temp_path = "C:/Users/vinic/Downloads/OEG-20220729T223604Z-001/OEG/iPhone/TEMP/temp.docx"
    doc.save(temp_path)

    convert(temp_path, directory)
    print("Converted!")

    os.remove(temp_path)

def create_pdf(modelo, serial, client_name, employee_name, color, problem):
    caminho_procura = 'C:/Users/vinic/Downloads/OEG-20220729T223604Z-001/OEG/iPhone'

    caminho_procura = concat(caminho_procura, modelo)
    if not os.path.exists(caminho_procura):
        os.mkdir(caminho_procura)
        caminho_procura = concat(caminho_procura, serial)
        os.mkdir(caminho_procura)
        salvar_PDF(caminho_procura, serial, client_name, employee_name, color, problem)
    else:
        caminho_procura = concat(caminho_procura, serial)
        if not os.path.exists(caminho_procura):
            os.mkdir(caminho_procura)
            salvar_PDF(caminho_procura, serial, client_name, employee_name, color, problem)
        else:
            salvar_PDF(caminho_procura, serial, client_name, employee_name, color, problem)
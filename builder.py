from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from etc import split_text_by_width
from dotenv import load_dotenv
import os
from path import PROGRAM_DIR

FONTS_DIR = os.path.join(PROGRAM_DIR, 'fonts')
RESULTS_DIR = os.path.join(PROGRAM_DIR, 'results')

pdfmetrics.registerFont(
    TTFont("GOST", os.path.join(FONTS_DIR, "GOST_0.TTF"))
)
pdfmetrics.registerFont(
    TTFont("GOST_I", os.path.join(FONTS_DIR, "GOST_I.ttf"))
)


def drawTitle(c, data):
  
  if data != None:
    customer_name = data.get("customer_name")
    tech_customer_name = data.get("tech_customer_name")
    general_contractor_name = data.get("general_contractor_name")
    contractor_name = data.get("contractor_name")
    object_name = data.get("object_name")
    project_name = data.get("project_name")
    project_cipher = data.get("project_cipher")
    copy_number = data.get("copy_number")
    number_of_volumes = data.get("number_of_volumes")
    volume_number = data.get("volume_number")
    city = data.get("city")
    year = data.get("year")
  else:
    return None
  
  # Рамка вокруг страницы
  c.setLineWidth(2.5)
  c.rect(5*mm, 5*mm, 200*mm, 287*mm, fill=0)
  
  # Номер экземпляра
  row = 15
  c.setFont('GOST', 18)
  c.drawRightString(200*mm, row*mm, copy_number)
  
  row += 15
  c.setFont('GOST', 24)
  c.drawCentredString(105*mm, row*mm, "Исполнительно-техническая документация")
  
  # Информация об организациях
  row += 15
  for element in [["Заказчик:", customer_name], \
                  ["Тех. заказчик:", tech_customer_name], \
                  ["Ген. подрядчик:", general_contractor_name], \
                  ["Подрядчик:", contractor_name]]:
    c.setFont('GOST', 16)
    c.drawRightString(50*mm, row*mm, element[0])
    name_wrap_lines = split_text_by_width(c, element[1], 'GOST_I', 18, 170*mm)
    c.setFont('GOST_I', 16)
    for line in name_wrap_lines:
      c.drawString(51*mm, row*mm, line)
      row+=7

  row += 10
  c.setFont('GOST', 24)
  c.drawCentredString(105*mm, row*mm, "Объект")

  # Наименование объекта
  row += 10
  c.setFont('GOST_I', 18)
  object_name_wrap_lines = split_text_by_width(c, object_name, 'GOST_I', 18, 180*mm)
  for line in object_name_wrap_lines:
    c.drawCentredString(105*mm, row*mm, line)
    row += 7

  row += 10
  c.setFont('GOST', 24)
  c.drawCentredString(105*mm, row*mm, "Раздел")

  # Наименование проекта
  row += 10
  c.setFont('GOST_I', 18)
  object_name_wrap_lines = split_text_by_width(c, project_name, 'GOST_I', 18, 180*mm)
  for line in object_name_wrap_lines:
    c.drawCentredString(105*mm, row*mm, line)
    row += 7
  
  # Шифр проекта
  row += 10
  c.setFont('GOST', 24)
  c.drawCentredString(105*mm, row*mm, project_cipher)

  if number_of_volumes != 1:
    # Кол-во книг   
    row += 30
    c.setFont('GOST', 24)
    c.drawCentredString(105*mm, row*mm, "Книга " + str(volume_number) + " из " + str(number_of_volumes))

  # Дата и место
  c.setFont('GOST', 18)
  c.drawCentredString(105*mm, 280*mm, "г. " + city + ", " + str(year) + "г.")

  c.showPage()
  return c


def drawSpine(c, data):
  
  if data != None:
    customer_name = data.get("customer_name")
    tech_customer_name = data.get("tech_customer_name")
    general_contractor_name = data.get("general_contractor_name")
    contractor_name = data.get("contractor_name")
    object_name = data.get("object_name")
    project_name = data.get("project_name")
    project_cipher = data.get("project_cipher")
    copy_number = data.get("copy_number")
    number_of_volumes = data.get("number_of_volumes")
    volume_number = data.get("volume_number")
    city = data.get("city")
    year = data.get("year")
  else:
    return None

  # Рамка корешка
  c.setLineWidth(1)
  # 110 x 50 мм
  c.rect(5*mm, 5*mm, 110*mm, 50*mm, fill=0)
  # 155 x 50 мм
  c.rect(5*mm, 60*mm, 155*mm, 50*mm, fill=0)
  # 110 x 31 мм
  c.rect(5*mm, 115*mm, 110*mm, 31*mm, fill=0)
  
  # Номер экземпляра
  c.setFont('GOST', 10)
  row = 10
  rows = [10, 119, 65]
  ## 110 x 50 мм
  c.drawRightString(112*mm, row*mm, copy_number)
  ## 110 x 31 мм
  c.drawRightString(114*mm, rows[1]*mm, "Ориг." if copy_number == "Оригинал" else copy_number)
  ## 155 x 50 мм
  c.setFont('GOST', 12)
  c.drawRightString(157*mm, rows[2]*mm, copy_number)

  # Тип документов
  c.setFont('GOST', 14)
  row += 5
  c.drawCentredString(57.5*mm, row*mm, "Исполнительно-техническая документация")
  c.drawCentredString(57.5*mm, rows[1]*mm, "Исполнительно-техническая документация")
  c.setFont('GOST', 16)
  c.drawCentredString(81.5*mm, rows[2]*mm, "Исполнительно-техническая документация")

  # Генподрядчик и подрядчик
  c.setFont('GOST', 10)
  rows = list(map(lambda row: row + 4, rows))
  row += 4
  ## 110 x 50 мм
  c.drawCentredString(57.5*mm, row*mm, f"{general_contractor_name} | {contractor_name}")
  ## 110 x 31 мм
  c.drawCentredString(57.5*mm, rows[1]*mm, f"{general_contractor_name} | {contractor_name}")
  ## 155 x 50 мм
  c.setFont('GOST', 12)
  rows[2] += 1
  c.drawCentredString(81.5*mm, rows[2]*mm, f"{general_contractor_name} | {contractor_name}")

  # Наименование объекта
  c.setFont('GOST_I', 12)
  rows = list(map(lambda row: row + 5, rows))
  row += 5
  ## 110 x 50 мм
  object_name_wrap_lines = split_text_by_width(c, object_name, 'GOST_I', 12, 110*mm)
  for line in object_name_wrap_lines:
    c.drawCentredString(59.5*mm, row*mm, line)
    row += 4
  ## 155 x 50 мм
  c.setFont('GOST_I', 14)
  object_name_wrap_lines = split_text_by_width(c, object_name, 'GOST_I', 14, 152*mm)
  for line in object_name_wrap_lines:
    c.drawCentredString(81.5*mm, rows[2]*mm, line)
    rows[2] += 5
  ## 110 x 31 мм
  c.setFont('GOST_I', 10)
  rows[1] -= 1
  object_name_wrap_lines = split_text_by_width(c, object_name, 'GOST_I', 10, 109*mm)
  for line in object_name_wrap_lines:
    c.drawCentredString(59.5*mm, rows[1]*mm, line)
    rows[1] += 4
  

  # Наименование проекта
  c.setFont('GOST_I', 10)
  row += 1
  rows[2] += 2
  ## 110 x 50 мм
  project_name_wrap_lines = split_text_by_width(c, project_name, 'GOST_I', 10, 110*mm)
  for line in project_name_wrap_lines:
    c.drawCentredString(59.5*mm, row*mm, line)
    row += 4
  ## 155 x 50 мм
  c.setFont('GOST_I', 14)
  project_name_wrap_lines = split_text_by_width(c, project_name, 'GOST_I', 14, 155*mm)
  for line in project_name_wrap_lines:
    c.drawCentredString(81.5*mm, rows[2]*mm, line)
    rows[2] += 5

  # Шифр проекта
  c.setFont('GOST_I', 12)
  c.drawCentredString(59.5*mm, row*mm, project_cipher)
  c.drawCentredString(59.5*mm, rows[1]*mm, project_cipher)
  c.setFont('GOST_I', 14)
  c.drawCentredString(81.5*mm, rows[2]*mm, project_cipher)

  # Информация о книгах
  if number_of_volumes != 1:
    string = "Книга " + str(volume_number) + " из " + str(number_of_volumes)
    rows = list(map(lambda row: row + 5, rows))
    row += 5
    ## 110 x 50 мм
    c.setFont('GOST', 12)
    c.drawCentredString(59.5*mm, row*mm, string)
    ## 155 x 50 мм
    c.setFont('GOST', 14)
    rows[2]+=1
    c.drawCentredString(81.5*mm, rows[2]*mm, string)
    ## 110 x 31 мм
    c.setFont('GOST', 12)
    rows[1] -= 1
    c.drawCentredString(59.5*mm, rows[1]*mm, string)
  
  c.showPage()
  return c


def generateNewFile(filename: str):
  path = os.path.join(RESULTS_DIR, f"{filename}.pdf")
  c = canvas.Canvas(path, pagesize=A4, bottomup=0)
  return [c, path]


def saveChangedFile(c):
  c.save()


def test_generator_module(data: dict):
  # Генерация нового файла
  newFile = generateNewFile("test_output")
  c = newFile[0]
  # Нарисовать титульную страницу
  c = drawTitle(c, data)
  # Нарисовать корешок
  c = drawSpine(c, data)
  # Сохранить изменения в файле
  saveChangedFile(c)


if __name__ == "__main__":
  load_dotenv()
  data = {
    "customer_name" : os.getenv("CUSTOMER"),
    "tech_customer_name" : os.getenv("TECH_CUSTOMER"),
    "general_contractor_name" : os.getenv("GEN_CONTRACTOR"),
    "contractor_name" : os.getenv("CONTRACTOR"),
    "object_name" : os.getenv("OBJECT"),
    "project_name" : os.getenv("PROJECT"),
    "project_cipher" : os.getenv("CIPHER"),
    "copy_number" : os.getenv("COPY"),
    "number_of_volumes" : os.getenv("NUMBER_OF_VOLUME"),
    "volume_number" : os.getenv("VOLUME_NUMBER"),
    "city" : os.getenv("CITY"),
    "year" : os.getenv("YEAR")
  }
  test_generator_module(data)
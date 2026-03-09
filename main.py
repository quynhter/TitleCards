import sys, os
from PySide6.QtWidgets import QApplication, QComboBox, QPushButton, QMessageBox, QLineEdit, QTextEdit, QSpinBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from datetime import datetime

from etc import add_sample, get_sample, get_all_samples, delete_current_sample
from builder import drawTitle, drawSpine, generateNewFile, saveChangedFile

from path import PROGRAM_DIR


RESULTS_DIR = os.path.join(PROGRAM_DIR, "results")
CONFIG_FILE = os.path.join(PROGRAM_DIR, 'config.json')
UI_FILE = os.path.join(PROGRAM_DIR, 'main.ui')

os.makedirs(RESULTS_DIR, exist_ok=True)
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write("[]")

def update_combo_samples():
  samples = get_all_samples()
  combo_samples = window.findChild(QComboBox, "samples")
  combo_samples.clear()
  sample_names = ['Новый шаблон...']
  for sample in samples:
      sample_names.append(sample.get('sample_name'))
  combo_samples.addItems(sample_names)


def load_sample():
  combo_samples = window.findChild(QComboBox, "samples")
  selected_sample = combo_samples.currentText()
  data = get_sample(selected_sample)

  sample_text_box = window.findChild(QLineEdit, "sample_text_box")
  object_text_box = window.findChild(QTextEdit, "object_text_box")
  project_text_box = window.findChild(QTextEdit, "project_text_box")
  cipher_text_box = window.findChild(QLineEdit, "cipher_text_box")
  customer_text_box = window.findChild(QLineEdit, "customer_text_box")
  tech_cust_text_box = window.findChild(QLineEdit, "tech_cust_text_box")
  gen_dev_text_box = window.findChild(QLineEdit, "gen_dev_text_box")
  dev_text_box = window.findChild(QLineEdit, "dev_text_box")
  city_text_box = window.findChild(QLineEdit, "city_text_box")
  copy_text_box = window.findChild(QSpinBox, "copy_text_box")
  vol_text_box = window.findChild(QSpinBox, "vol_text_box")
  year_text_box = window.findChild(QSpinBox, "year_text_box")

  if selected_sample == "Новый шаблон...":
    sample_text_box.setText("")
    object_text_box.setText("")
    project_text_box.setText("")
    cipher_text_box.setText("")
    customer_text_box.setText("")
    tech_cust_text_box.setText("")
    gen_dev_text_box.setText("")
    dev_text_box.setText("")
    city_text_box.setText("")
    year_text_box.setValue(2025)
    copy_text_box.setValue(5)
    vol_text_box.setValue(1)
  else:
    sample_text_box.setText(data.get('sample_name'))
    object_text_box.setText(data.get('object_name'))
    project_text_box.setText(data.get('project_name'))
    cipher_text_box.setText(data.get('project_cipher'))
    customer_text_box.setText(data.get('customer_name'))
    tech_cust_text_box.setText(data.get('tech_customer_name'))
    gen_dev_text_box.setText(data.get('general_contractor_name'))
    dev_text_box.setText(data.get('contractor_name'))
    city_text_box.setText(data.get('city'))
    year_text_box.setValue(data.get('year'))
    copy_text_box.setValue(data.get('copies'))
    vol_text_box.setValue(data.get('volumes'))


def save_sample():
  sample_text_box = window.findChild(QLineEdit, "sample_text_box")
  object_text_box = window.findChild(QTextEdit, "object_text_box")
  project_text_box = window.findChild(QTextEdit, "project_text_box")
  cipher_text_box = window.findChild(QLineEdit, "cipher_text_box")
  customer_text_box = window.findChild(QLineEdit, "customer_text_box")
  tech_cust_text_box = window.findChild(QLineEdit, "tech_cust_text_box")
  gen_dev_text_box = window.findChild(QLineEdit, "gen_dev_text_box")
  dev_text_box = window.findChild(QLineEdit, "dev_text_box")
  city_text_box = window.findChild(QLineEdit, "city_text_box")
  copy_text_box = window.findChild(QSpinBox, "copy_text_box")
  vol_text_box = window.findChild(QSpinBox, "vol_text_box")
  year_text_box = window.findChild(QSpinBox, "year_text_box")
  
  samples = get_all_samples()
  if sample_text_box.text() == "" or \
      object_text_box.toPlainText() == "" or \
      project_text_box.toPlainText() == "" or \
      cipher_text_box.text() == "" or \
      customer_text_box.text() == "" or \
      tech_cust_text_box.text() == "" or \
      gen_dev_text_box.text() == "" or \
      dev_text_box.text() == "" or \
      city_text_box.text() == "":
    QMessageBox.information(window, "Действие", "Некоторые поля пустые\nСохранить шаблон не получится")
  if len(samples) == 0:
    data = {
      "sample_name": sample_text_box.text(),
      "customer_name": customer_text_box.text(),
      "tech_customer_name": tech_cust_text_box.text(),
      "general_contractor_name": gen_dev_text_box.text(),
      "contractor_name": dev_text_box.text(),
      "object_name": object_text_box.toPlainText(),
      "project_name": project_text_box.toPlainText(),
      "project_cipher": cipher_text_box.text(),
      "copies": copy_text_box.value(),
      "volumes": vol_text_box.value(),
      "city": city_text_box.text(),
      "year": year_text_box.value(),
    }
    add_sample(data)
    update_combo_samples()
    return
  else:
    for sample in samples:
      if sample_text_box.text() == sample.get('sample_name'):
        msg = QMessageBox(window)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Подтверждение")
        msg.setText("Такой шаблон уже существует.\nЗаменить его?")

        yes_btn = msg.addButton("Заменить", QMessageBox.AcceptRole)
        no_btn = msg.addButton("Отмена", QMessageBox.RejectRole)

        msg.exec()

        if msg.clickedButton() == yes_btn:
          data = {
              "sample_name": sample_text_box.text(),
              "customer_name": customer_text_box.text(),
              "tech_customer_name": tech_cust_text_box.text(),
              "general_contractor_name": gen_dev_text_box.text(),
              "contractor_name": dev_text_box.text(),
              "object_name": object_text_box.toPlainText(),
              "project_name": project_text_box.toPlainText(),
              "project_cipher": cipher_text_box.text(),
              "copies": copy_text_box.value(),
              "volumes": vol_text_box.value(),
              "city": city_text_box.text(),
              "year": year_text_box.value(),
          }
          add_sample(data)
          return None
        else:
          return None
      else:
        data = {
          "sample_name": sample_text_box.text(),
          "customer_name": customer_text_box.text(),
          "tech_customer_name": tech_cust_text_box.text(),
          "general_contractor_name": gen_dev_text_box.text(),
          "contractor_name": dev_text_box.text(),
          "object_name": object_text_box.toPlainText(),
          "project_name": project_text_box.toPlainText(),
          "project_cipher": cipher_text_box.text(),
          "copies": copy_text_box.value(),
          "volumes": vol_text_box.value(),
          "city": city_text_box.text(),
          "year": year_text_box.value(),
        }
        add_sample(data)
    update_combo_samples()


def delete_sample():
  combo_samples = window.findChild(QComboBox, "samples")
  selected_sample = combo_samples.currentText()
  if selected_sample == "Новый шаблон...":
    QMessageBox.information(window, "Действие", "Новый шаблон нельзя удалить")
  else:
    msg = QMessageBox(window)
    msg.setIcon(QMessageBox.Question)
    msg.setWindowTitle("Подтверждение")
    msg.setText("Вы уверены?")
    
    yes_btn = msg.addButton("Удалить", QMessageBox.AcceptRole)
    no_btn = msg.addButton("Отмена", QMessageBox.RejectRole)
    
    msg.exec()
    
    if msg.clickedButton() == yes_btn:
      deleted = delete_current_sample(selected_sample)
      QMessageBox.information(window, "Информация", deleted)
  update_combo_samples()


def create_PDF():
  if os.path.exists('fonts/GOST_0.TTF') == False or os.path.exists('fonts/GOST_I.ttf') == False:
    QMessageBox.information(window, "Ошибка", "Отсутствует полный комплект шрифтов для продолжения операции \nУбедитесь, что необходимые шрифты находятся по пути:\nfonts/GOST_0.TTF\nfonts/GOST_I.ttf")
    return None
  combo_samples = window.findChild(QComboBox, "samples")
  selected_sample = combo_samples.currentText()
  data = get_sample(selected_sample)
  
  sample_text_box = window.findChild(QLineEdit, "sample_text_box")
  object_text_box = window.findChild(QTextEdit, "object_text_box")
  project_text_box = window.findChild(QTextEdit, "project_text_box")
  cipher_text_box = window.findChild(QLineEdit, "cipher_text_box")
  customer_text_box = window.findChild(QLineEdit, "customer_text_box")
  tech_cust_text_box = window.findChild(QLineEdit, "tech_cust_text_box")
  gen_dev_text_box = window.findChild(QLineEdit, "gen_dev_text_box")
  dev_text_box = window.findChild(QLineEdit, "dev_text_box")
  city_text_box = window.findChild(QLineEdit, "city_text_box")
  copy_text_box = window.findChild(QSpinBox, "copy_text_box")
  vol_text_box = window.findChild(QSpinBox, "vol_text_box")
  year_text_box = window.findChild(QSpinBox, "year_text_box")
  
  if sample_text_box.text() == "" or \
        object_text_box.toPlainText() == "" or \
        project_text_box.toPlainText() == "" or \
        cipher_text_box.text() == "" or \
        customer_text_box.text() == "" or \
        tech_cust_text_box.text() == "" or \
        gen_dev_text_box.text() == "" or \
        dev_text_box.text() == "":
    QMessageBox.information(window, "Действие", "Некоторые поля пустые\nСоздать PDF не получится")
  else:
    newFile = generateNewFile(filename=sample_text_box.text())
    c = newFile[0]
    path = f"{newFile[1]}"
    data = {
        "sample_name": sample_text_box.text(),
        "customer_name": customer_text_box.text(),
        "tech_customer_name": tech_cust_text_box.text(),
        "general_contractor_name": gen_dev_text_box.text(),
        "contractor_name": dev_text_box.text(),
        "object_name": object_text_box.toPlainText(),
        "project_name": project_text_box.toPlainText(),
        "project_cipher": cipher_text_box.text(),
        "copy_number": copy_text_box.value(),
        "number_of_volumes": vol_text_box.value(),
        "volume_number": 1,
        "city": city_text_box.text(),
        "year": year_text_box.value()
    }
    if copy_text_box.value() == 1:
        data['copy_number'] = "Оригинал"
        for i in range(vol_text_box.value()):
            data['volume_number'] = i + 1
            if vol_text_box.value() == 1:
              c = drawTitle(c, data)
              с = drawSpine(c, data)
            else:
              for j in range(1, vol_text_box.value() + 1):
                data['volume_number'] = j
                c = drawTitle(c, data)
                с = drawSpine(c, data)
    else:
        for i in range(1, copy_text_box.value() + 1):
          if i == 1:
            data['copy_number'] = "Оригинал"
          else:
            data['copy_number'] = f"{i} экз."
          for j in range(1, vol_text_box.value() + 1):
            data['volume_number'] = j
            c = drawTitle(c, data)
            с = drawSpine(c, data)
    saveChangedFile(c)
    QMessageBox.information(window, "Действие", f"Файл успешно создан по пути: \n{path}")


app = QApplication(sys.argv)

ui_path = UI_FILE
ui_file = QFile(ui_path)
if not ui_file.open(QFile.ReadOnly):
    raise RuntimeError(f"Не удалось открыть UI файл: {ui_path}")
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

update_combo_samples()

# Определение функций для кнопок
loadSample_button = window.findChild(QPushButton, "loadSample").clicked.connect(load_sample)
saveSample_button = window.findChild(QPushButton, "saveSample").clicked.connect(save_sample)
deleteSample_button = window.findChild(QPushButton, "deleteSample").clicked.connect(delete_sample)
createPDF_button = window.findChild(QPushButton, "createPDF").clicked.connect(create_PDF)

window.findChild(QSpinBox, "year_text_box").setValue(datetime.now().year)

window.show()

sys.exit(app.exec())

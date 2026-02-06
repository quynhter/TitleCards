import json
import os
from path import PROGRAM_DIR

filename = os.path.join(PROGRAM_DIR, 'config.json')

def add_sample(data):
  if os.path.exists(filename):
    try:
      with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        if content.strip():
          samples = json.loads(content)
        else:
          samples = []
    except json.JSONDecodeError as e:
      print(f"Ошибка парсинга JSON из {filename}: {e}")
      samples = []
  else:
    samples = []
  key = 'sample_name'
  for i, d in enumerate(samples):
    if d.get(key) == data.get(key):
      del samples[i]
      break
  samples.append(data)
  with open(filename, 'w', encoding='utf-8') as file:
    json.dump(samples, file, ensure_ascii=False, indent=4)

def delete_current_sample(sample_name: str) -> str:
  if os.path.exists(filename):
    try:
      with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        if content.strip():
          samples = json.loads(content)
        else:
           return "Конфиг пока не содержит ни один шаблон"
    except json.JSONDecodeError as e:
      return f"Ошибка парсинга JSON из {filename}: {e}"
  key = 'sample_name'
  for i, d in enumerate(samples):
     if d.get(key) == sample_name:
        del samples[i]
        break
  with open(filename, 'w', encoding='utf-8') as file:
    json.dump(samples, file, ensure_ascii=False, indent=4)
  return "Шаблон успешно удален"
    

def get_sample(sample_name: str):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():
                    samples = json.loads(content)
                    for sample in samples:
                        if sample['sample_name'] == sample_name:
                            return sample
                else:
                    return None
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON из {filename}: {e}")
            return None

def get_all_samples():
  samples = []
  if os.path.exists(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            if content.strip():
                samples = json.loads(content)
            else:
                return None
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON из {filename}: {e}")
        return None
  return samples

def split_text_by_width(canvas, text, font, size, max_width):
    # Разбивает текст на строки, которые помещаются в max_width
    words = text.split()
    lines = []
    current_line = words[0] if words else ""
    
    for word in words[1:]:
        test_line = current_line + " " + word
        # Проверяем ширину строки
        if canvas.stringWidth(test_line, font, size) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def test_etc_module():
    print("1 - get_all_samples")
    print("2 - get_sample")
    choice = input('\nВаш выбор: ')
    if choice == '1':
        print(get_all_samples())
    elif choice == '2':
        while True:
            choice = input('\nВведите sample_name (bye - завершить программу): ')
            if choice == 'bye':
                break
            result = get_sample(choice)
            if result == None:
                print('Шаблона с таким sample_name нет')
            else:
                print(result)
                break


if __name__ == "__main__":
    test_etc_module()
import os
import shutil
from pathlib import Path

nested_path = Path("Workspace/Projects/TextFiles")
nested_path.mkdir(parents=True, exist_ok=True)

for item in os.listdir('.'):
    print(f"{item}")


all_items = os.listdir('.')
txt_files = list(filter(lambda x: x.endswith('.txt'), all_items))
print(f"Все текстовые файлы: {txt_files}")


for file_name in txt_files:
    source = file_name
    destination = nested_path / file_name
    
    shutil.copy2(source, destination)
    print(f"Скопировал: {file_name} -> {destination}")


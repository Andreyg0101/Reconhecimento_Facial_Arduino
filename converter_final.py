from PIL import Image
import os

# Caminho da pasta onde estão as fotos
base_path = r"C:\Users\ediso\Videos\projeto_acesso"

# Lista de arquivos originais e convertidos
nomes = ["andrey", "lucas", "pontinho", "belmonte", "vinicius"]

for nome in nomes:
    input_path = os.path.join(base_path, f"{nome}.jpg")
    output_path = os.path.join(base_path, f"{nome}_ok.jpg")

    if os.path.exists(input_path):
        try:
            img = Image.open(input_path).convert("RGB")  # Força RGB 8-bit
            img.save(output_path, format="JPEG", quality=95)
            print(f"✅ {output_path} salvo com sucesso (RGB 8-bit).")
        except Exception as e:
            print(f"❌ Erro ao converter {nome}: {e}")
    else:
        print(f"⚠️ {input_path} não encontrado.")

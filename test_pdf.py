
from pdf_reader import extract_text_from_pdf

file_path = input("Enter PDF file path: ").strip().strip('"')

with open(file_path, "rb") as pdf_file:
    text = extract_text_from_pdf(pdf_file)

print("\nExtracted PDF Text:")
print("-------------------")
print(text[:3000])

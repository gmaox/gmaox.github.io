# 将PDF按A4拆分的py代码
```
import fitz  # pip install pymupdf
import os

# A4竖页尺寸（单位：pt）
a4_width, a4_height = 595, 842

input_dir = "."
output_dir = "./new"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        doc = fitz.open(input_path)
        new_doc = fitz.open()

        for page in doc:
            width, height = page.rect.width, page.rect.height
            scale = a4_width / width  # 按宽度缩放
            scaled_height = height * scale
            num_splits = int(scaled_height // a4_height) + (1 if scaled_height % a4_height > 0 else 0)

            for i in range(num_splits):
                # 计算原页面中当前A4区域对应的裁剪区域
                y0 = (i * a4_height) / scale
                y1 = min(height, ((i + 1) * a4_height) / scale)
                clip_rect = fitz.Rect(0, y0, width, y1)
                # 计算目标区域高度
                part_scaled_height = (y1 - y0) * scale
                # 顶部对齐
                target_rect = fitz.Rect(0, 0, a4_width, part_scaled_height)
                new_page = new_doc.new_page(width=a4_width, height=a4_height)
                new_page.show_pdf_page(
                    target_rect,
                    doc, page.number, clip=clip_rect
                )

        new_doc.save(output_path)
        new_doc.close()
```
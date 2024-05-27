import streamlit as st
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import os

# Class for handling image upload and display
class ImageUploader:
    def __init__(self):
        self.uploaded_file = None

    def upload_image(self):
        self.uploaded_file = st.file_uploader("Sube tu imagen", type=["png", "jpg", "jpeg", "pdf", "docx", "pptx", "bmp", "gif", "tif"])
        return self.uploaded_file

    def display_image_info(self):
        if self.uploaded_file:
            image = Image.open(self.uploaded_file)
            st.image(image, caption='Imagen subida', use_column_width=True)
            file_info = {
                "name": self.uploaded_file.name,
                "size": self.uploaded_file.size,
                "format": self.uploaded_file.type
            }
            return file_info
        return None

# Class for format selection
class FormatSelector:
    def __init__(self):
        self.formats = ["pdf", "docx", "pptx", "bmp", "gif", "jpg", "tif", "png"]
        self.selected_format = None

    def display_format_selector(self):
        self.selected_format = st.selectbox("Selecciona el formato de conversión", self.formats)
        return self.selected_format

# Class for handling image conversion
class ImageConverter:
    def __init__(self, image_path):
        self.image_path = image_path

    def convert_image(self, target_format):
        img = Image.open(self.image_path)
        output_path = f"output.{target_format}"
        if target_format == "pdf":
            pdf = canvas.Canvas(output_path)
            ruta_imagen = os.path.abspath(self.image_path)
            pdf.drawImage(ruta_imagen, 0, 0, width=img.width, height=img.height)
            pdf.save()
        else:
            img.save(output_path)
        return output_path

# Class for handling image editing
class ImageEditor:
    def __init__(self, image_path):
        self.image_path = image_path

    def edit_image(self):
        # Placeholder for editing functionality
        pass

# Class for adding watermark to image
class Watermarker:
    def __init__(self, image_path):
        self.image_path = image_path

    def add_watermark(self, text="@tarea"):
        img = Image.open(self.image_path).convert("RGBA")
        txt = Image.new('RGBA', img.size, (255, 255, 255, 0))

        font = ImageFont.load_default()
        draw = ImageDraw.Draw(txt)

        # Get text bounding box
        textbbox = draw.textbbox((0, 0), text, font=font)
        textwidth = textbbox[2] - textbbox[0]
        textheight = textbbox[3] - textbbox[1]
        width, height = img.size

        x = (width - textwidth) / 2
        y = (height - textheight) / 2

        draw.text((x, y), text, fill=(255, 255, 255, 128), font=font)
        watermarked = Image.alpha_composite(img, txt)

        watermarked_path = "watermarked.png"
        watermarked.save(watermarked_path, "PNG")
        return watermarked_path

# Main function to run the Streamlit app
def main():
    st.title("Convertir Imagen")
    
    image_uploader = ImageUploader()
    uploaded_file = image_uploader.upload_image()
    
    if uploaded_file:
        file_info = image_uploader.display_image_info()
        
        if file_info:
            st.write(f"Nombre: {file_info['name']}")
            st.write(f"Tamaño: {file_info['size']} bytes")
            st.write(f"Formato: {file_info['format']}")
            
            format_selector = FormatSelector()
            selected_format = format_selector.display_format_selector()
            
            if st.button("Convertir"):
                temp_image_path = f"temp_image.{file_info['format'].split('/')[1]}"
                with open(temp_image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                image_converter = ImageConverter(temp_image_path)
                converted_path = image_converter.convert_image(selected_format)
                
                watermarker = Watermarker(converted_path)
                watermarked_path = watermarker.add_watermark()
                
                st.image(watermarked_path, caption='Imagen convertida y con marca de agua', use_column_width=True)
                
                with open(watermarked_path, "rb") as file:
                    btn = st.download_button(
                        label="Descargar imagen convertida",
                        data=file,
                        file_name=f"output.{selected_format}",
                        mime=f"image/{selected_format}" if selected_format != "pdf" else "application/pdf"
                    )

if __name__ == "__main__":
    main()

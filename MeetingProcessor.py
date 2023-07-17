from pytube import YouTube
from pydub import AudioSegment
import whisper
import openai
import os
import textwrap
from tqdm import tqdm
import subprocess
import shutil
import getpass
from google.colab import files



class Meet:

    def __init__(self, url_o_ruta):
        self.url_o_ruta = url_o_ruta

    def download_video(self):
        youtube = YouTube(self.url_o_ruta)
        video = youtube.streams.get_highest_resolution()
        video.download(output_path='/content', filename='video.mp4')
        return '/content/video.mp4'

    def video2audio(self, ruta_video):
        video = AudioSegment.from_file(ruta_video, "mp4")
        ruta_audio = 'audio.mp3'
        video.export(ruta_audio, format="mp3")
        return ruta_audio

    def audio2text(self, ruta_audio):
        model = whisper.load_model("large")
        result = model.transcribe(ruta_audio)
        texto = result["text"]
        ruta_transcripcion = 'transcripcion.txt'
        with open(ruta_transcripcion, 'w') as f:
            f.write(texto)
        return ruta_transcripcion

    def text_processing(self, ruta_transcripcion):
        with open(ruta_transcripcion, 'r') as f:
            texto = f.read()
        print("Please enter your OpenAI API key:")
        openai.api_key = getpass.getpass()
        fragmentos_texto = textwrap.wrap(texto, 3000)
        respuestas = []
        for fragmento in fragmentos_texto:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""Actúa como un secretario de actas con experiencia, te daré un fragmento de texto de una reunión, quiero que me entregues un resumen en formato LaTeX que debe tener la siguiente estructura.\\section{{parte {fragmentos_texto.index(fragmento)+1}}} \\subsection{{Tema}} \\subsection{{Agenda}} \\subsection{{Decisiones}} \\subsection{{Compromisos}}, el contenido de la subsección Tema puedes ser un breve resumen, el contenido de la subsección Agenda debe ser los temas mas importantes que se mencionaron separados por comas, el contenido de la subsección Decisiones debe tener los temas de las decisiones mas importantes separados por comas y el contenido de la subsección Compromisos debe establecer los compromisos y si es posible con su responsable y fechas separados por comas, si no existe contenido en una subsección puedes escribir que no se establecieron en esa parte, no cambies el formato LaTeX establecido, no uses un entorno itimize, numerate o description,recuerda que lo que me entregues se colocará entre un \\begin{{document}} y \\end{{document}} que ya tiene su preámbulo Latex"""},
                    {"role": "user", "content": fragmento}
                ],
                temperature=0.5,
                max_tokens=300,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            respuestas.append(response['choices'][0]['message']['content'])
        ruta_respuestas = 'respuestas.txt'
        with open(ruta_respuestas, 'w') as f:
            for respuesta in respuestas:
                f.write(f"{respuesta}\n")
        return ruta_respuestas

    def latex_document(self, file_name):
        start_document = [
            "\\documentclass{article}",
            "\\usepackage[spanish]{babel}",
            "\\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}",
            "\\begin{document}",
        ]
        end_document = "\\end{document}"
        base_file_name, _ = os.path.splitext(file_name)
        temp_file = f"{base_file_name}_temp.tex"
        with open(temp_file, "w") as tex_file:
            with open(file_name, "r") as content_file:
                content = content_file.read()
                if not content.startswith("\\documentclass{article}"):
                    for line in start_document:
                        tex_file.write(line + "\n")
                tex_file.write(content)
                if not content.endswith(end_document):
                    tex_file.write("\n" + end_document)
        os.remove(file_name)
        new_file_name = base_file_name + '.tex'
        os.rename(temp_file, new_file_name)
        return new_file_name

    def convert_pdf(self, filename_tex):
        tex_filename = filename_tex if filename_tex.endswith('.tex') else filename_tex + ".tex"
        pdf_filename = os.path.splitext(tex_filename)[0] + '.pdf'
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], capture_output=True, text=True)
        if os.path.exists(pdf_filename):
            new_pdf_filename = 'acta_reunion.pdf'
            shutil.move(pdf_filename, new_pdf_filename)
            return new_pdf_filename
        print("PDF file not found. The LaTeX file might have severe errors that prevented PDF generation.")
        return None

    def download_file(self, ruta_archivo):
        files.download(ruta_archivo)

    def process(self):
        if 'youtube' in self.url_o_ruta:
            with tqdm(total=1, desc="Downloading video from YouTube", disable=False) as pbar:
                ruta_video = self.download_video()
                pbar.update(1)
        else:
            ruta_video = self.url_o_ruta

        with tqdm(total=1, desc="Converting video to audio", disable=False) as pbar:
            ruta_audio = self.video2audio(ruta_video)
            pbar.update(1)

        print("Transcribing audio with Whisper...")
        ruta_transcripcion = self.audio2text(ruta_audio)

        with tqdm(total=1, desc="Processing text with GPT-4", disable=False) as pbar:
            ruta_respuestas = self.text_processing(ruta_transcripcion)
            pbar.update(1)

        with tqdm(total=1, desc="Creating LaTeX document", disable=False) as pbar:
            ruta_latex = self.latex_document(ruta_respuestas)
            pbar.update(1)

        with tqdm(total=1, desc="Converting LaTeX Document to PDF", disable=False) as pbar:
            ruta_pdf = self.convert_pdf(ruta_latex)
            pbar.update(1)

        with tqdm(total=1, desc="Downloading PDF document", disable=False) as pbar:
            self.download_file(ruta_pdf)
            pbar.update(1)

        return ruta_pdf
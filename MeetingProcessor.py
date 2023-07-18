import os
import getpass
import textwrap
import subprocess
import concurrent.futures
from pytube import YouTube
from pydub import AudioSegment
from tqdm import tqdm
from IPython.display import FileLink
from pdf2docx import Converter
import whisper
import openai


class Meet:

    def __init__(self, url_or_path):
        self.url_or_path = url_or_path
        self.api_key = None
        self.audio_path = None
        self.transcription_path = None
        self.response_path = None
        self.latex_path = None
        self.pdf_path = None
        self.docx_path = None

    @staticmethod
    def download_file(file_path):
        try:
            from google.colab import files
            files.download(file_path)
        except ImportError:
            display(FileLink(file_path))

    @staticmethod
    def download_video(url):
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video.download(output_path='/content', filename='video.mp4')

    @staticmethod
    def video2audio(video_path):
        video = AudioSegment.from_file(video_path, "mp4")
        audio_path = 'audio.mp3'
        video.export(audio_path, format="mp3")
        return audio_path

    @staticmethod
    def audio2text(audio_path):
        model = whisper.load_model("large")
        result = model.transcribe(audio_path)
        text = result["text"]
        transcription_path = 'transcription.txt'
        with open(transcription_path, 'w') as f:
            f.write(text)
        return transcription_path

    def text_processing(self, transcription_path):
        with open(transcription_path, 'r') as f:
            text = f.read()
        openai.api_key = self.api_key
        text_fragments = textwrap.wrap(text, 3000)
        responses = []
        for fragment in text_fragments:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""Actúa como un secretario de actas con experiencia, te daré un fragmento de texto de una reunión, quiero que me entregues un resumen en formato LaTeX que debe tener la siguiente estructura.\\section{{parte {text_fragments.index(fragment)+1}}} \\subsection{{Tema}} \\subsection{{Agenda}} \\subsection{{Decisiones}} \\subsection{{Compromisos}}, el contenido de la subsección Tema puedes ser un breve resumen, el contenido de la subsección Agenda debe ser los temas mas importantes que se mencionaron separados por comas, el contenido de la subsección Decisiones debe tener los temas de las decisiones mas importantes separados por comas y el contenido de la subsección Compromisos debe establecer los compromisos y si es posible con su responsable y fechas separados por comas, si no existe contenido en una subsección puedes escribir que no se establecieron en esa parte, no cambies el formato LaTeX establecido, no uses un entorno itimize, numerate o description,recuerda que lo que me entregues se colocará entre un \\begin{{document}} y \\end{{document}} que ya tiene su preámbulo Latex"""},
                    {"role": "user", "content": fragment}
                ],
                temperature=0.5,
                max_tokens=300,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            responses.append(response['choices'][0]['message']['content'])
        response_path = 'responses.txt'
        with open(response_path, 'w') as f:
            for response in responses:
                f.write(f"{response}\n")
        return response_path

    @staticmethod
    def latex_document(response_path):
        start_document = [
            "\\documentclass{article}",
            "\\usepackage[spanish]{babel}",
            "\\usepackage[utf8]{inputenc}",
            "\\usepackage[T1]{fontenc}",
            "\\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}",
            "\\begin{document}",
        ]
        end_document = "\\end{document}"
        base_file_name, _ = os.path.splitext(response_path)
        temp_file = f"{base_file_name}_temp.tex"
        with open(temp_file, "w") as tex_file:
            with open(response_path, "r") as content_file:
                content = content_file.read()
                if not content.startswith("\\documentclass{article}"):
                    for line in start_document:
                        tex_file.write(line + "\n")
                tex_file.write(content)
                if not content.endswith(end_document):
                    tex_file.write("\n" + end_document)
        os.remove(response_path)
        new_file_name = base_file_name + '.tex'
        os.rename(temp_file, new_file_name)
        return new_file_name

    @staticmethod
    def convert_pdf(tex_filename):
        pdf_filename = os.path.splitext(tex_filename)[0] + '.pdf'
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], capture_output=True)
        output = result.stdout.decode('utf-8', errors='replace')
        if os.path.exists(pdf_filename):
            print(f"PDF file {pdf_filename} created successfully.")
            return pdf_filename
        print("PDF file not found. The LaTeX file may have severe errors that prevented the PDF from being generated.")
        return None

    @staticmethod
    def pdf2docx(pdf_path):
        cv = Converter(pdf_path)
        docx_file = "meeting_minutes.docx"
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        return docx_file

    def process(self):
        print("Please enter your OpenAI API key:")
        self.api_key = getpass.getpass()
        if 'youtube' in self.url_or_path:
            with tqdm(total=1, desc="Downloading video from YouTube", disable=False) as pbar:
                self.download_video(self.url_or_path)
                pbar.update(1)
            video_path = '/content/video.mp4'
        else:
            video_path = self.url_or_path
        with tqdm(total=1, desc="Converting video to audio", disable=False) as pbar:
            self.audio_path = self.video2audio(video_path)
            pbar.update(1)
        print("Transcribing audio with Whisper...")
        self.transcription_path = self.audio2text(self.audio_path)
        with tqdm(total=1, desc="Processing text with GPT-4", disable=False) as pbar:
            self.response_path = self.text_processing(self.transcription_path)
            pbar.update(1)

        with tqdm(total=1, desc="Creating LaTeX document", disable=False) as pbar:
            self.latex_path = self.latex_document(self.response_path)
            pbar.update(1)

        with tqdm(total=1, desc="Converting LaTeX Document to PDF", disable=False) as pbar:
            self.pdf_path = self.convert_pdf(self.latex_path)
            pbar.update(1)

        if self.pdf_path is None:
            print(f"Failed to convert LaTeX to PDF after 2 retries.")
            return None

        with tqdm(total=1, desc="Converting PDF to Word document", disable=False) as pbar:
            self.docx_path = self.pdf2docx(self.pdf_path)
            pbar.update(1)

        with tqdm(total=1, desc="Downloading Word document", disable=False) as pbar:
            self.download_file(self.docx_path)
            pbar.update(1)

        return self.docx_path


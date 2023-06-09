from fpdf import FPDF
from lib import config
from lib.ai import messages, io
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        width = self.get_string_width(self.title) + 6
        self.cell(txt=self.title, align="C")
        self.ln(10)

    def footer(self):
        # Setting position at 1.5 cm from bottom:
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def user_message(self, message):
        self.set_font("helvetica", "", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(txt='User')
        self.ln(4)
        self.cell(txt=message)
        self.ln(4)

    def assistant_message(self, message):
        self.set_font("helvetica", "", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(txt='Assistant')
        self.ln(4)
        self.cell(txt=message)
        self.ln(4)

    def add_messages(self, chat_messages):
        for part in chat_messages:
            if part['role'] == 'user':
                self.user_message(part['content'])
            else:
                self.assistant_message(part['content'])




def export_chat_to_pdf(file_name: str = None, chat_index: int = 0) -> None:
    file_path = config.get_export_path() / file_name
    dt = datetime.now()
    date_str = dt.strftime('%Y-%m-%d')
    time_str = dt.strftime('%H:%M:%S')
    title = f'# ChatGPT | {config.get_text_model_name()} | {date_str} | {time_str}\n'

    pdf = PDF()
    pdf.set_title(title)
    pdf.add_page()
    pdf.add_messages(messages.chat)
    pdf.output(str(file_path))
    io.open_file(file_path=file_path)
    return
    pdf = FPDF()
    pdf.set_font('helvetica', size=12)

    pdf.cell(txt=title)

    def chat_to_cells(chat_messages):
        for part in chat_messages:
            if part['role'] == 'user':
                pdf.cell(txt=f'## User')
            else:
                pdf.cell(txt=f'## Assistant')
            pdf.cell(txt=part['content'])

    chat_index = int(chat_index)
    if chat_index == 0:
        chat_to_cells(messages.chat)
    else:
        indexOffset = chat_index * 2
        chat_to_cells(messages.chat[-indexOffset:])


    pdf.output(str(file_path))
    io.open_file(file_path=file_path)

def convert_to_pdf(html) -> bytearray:
    pdf = FPDF()
    pdf.add_page()
    pdf.write_html(html)
    return pdf.output()
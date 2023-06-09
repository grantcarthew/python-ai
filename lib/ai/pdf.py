from fpdf import FPDF
from lib import config
from lib.ai import messages, io
from datetime import datetime
from rich import print as rprint


class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        width = self.get_string_width(self.title) + 6
        self.cell(txt=self.title, align="C")
        self.ln(10)
        self.set_line_width(0.4)
        self.line(0, self.get_y(), self.w, self.get_y())
        self.ln(7)

    def footer(self):
        # Setting position at 1.5 cm from bottom:
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_line(self, break_size: int):
        self.ln(break_size)
        self.set_line_width(0.4)
        self.line(0, self.get_y(), self.w, self.get_y())
        self.ln(break_size * 0.7)

    def user_message(self, message):
        self.set_font("helvetica", "", 12)
        self.set_fill_color(200, 220, 255)
        self.set_font(style="B")
        self.ln(5)
        self.cell(txt='User', markdown=True)
        self.add_line(6)
        self.set_font(style="")
        self.multi_cell(w=0, txt=message, markdown=True)
        self.add_line(6)

    def assistant_message(self, message):
        self.set_font("helvetica", "", 12)
        self.set_fill_color(200, 220, 255)
        self.set_font(style="B")
        self.ln(5)
        self.cell(txt='Assistant', markdown=True)
        self.add_line(6)
        self.set_font(style="")
        self.multi_cell(w=0, txt=message, markdown=True)
        self.add_line(6)

    def add_messages(self, chat_messages):
        for part in chat_messages:
            if part['role'] == 'user':
                self.user_message(part['content'])
            else:
                self.assistant_message(part['content'])


def convert_chat_to_pdf(chat_index: int = 0) -> None:
    dt = datetime.now()
    date_str = dt.strftime('%Y-%m-%d')
    time_str = dt.strftime('%H:%M:%S')
    title = f'# ChatGPT | {config.get_text_model_name()} | {date_str} | {time_str}\n'

    pdf = PDF()
    pdf.set_title(title)
    pdf.add_page()
    pdf.add_messages(messages.chat)

    return pdf.output()

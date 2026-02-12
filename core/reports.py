from fpdf import FPDF
import textwrap


def sanitize_text(text: str) -> str:
    """
    Converts Unicode characters into latin-1 safe equivalents
    so FPDF does not crash.
    """

    replacements = {
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2014": "-",   # em dash
        "\u2013": "-",   # en dash
        "\u2026": "...", # ellipsis
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    # Remove remaining unsupported characters
    return text.encode("latin-1", "ignore").decode("latin-1")


class ReportBuilder:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.margin_left = 15
        self.margin_right = 15
        self.page_width = 210 - self.margin_left - self.margin_right

    # ----------------------------
    # Core Layout Helpers
    # ----------------------------

    def _add_new_page(self):
        self.pdf.add_page()
        self.pdf.set_left_margin(self.margin_left)
        self.pdf.set_right_margin(self.margin_right)

    def _add_horizontal_rule(self):
        y = self.pdf.get_y()
        self.pdf.line(self.margin_left, y, 210 - self.margin_right, y)
        self.pdf.ln(5)

    # ----------------------------
    # Public Methods
    # ----------------------------

    def add_title(self, title: str):
        self._add_new_page()
        self.pdf.set_font("Arial", "B", 18)
        self.pdf.cell(0, 10, sanitize_text(title), ln=True)
        self.pdf.ln(4)
        self._add_horizontal_rule()

    def add_section(self, header: str, body: str):
        self.pdf.ln(6)
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.multi_cell(0, 8, sanitize_text(header))
        self.pdf.ln(2)

        self.pdf.set_font("Arial", "", 11)

        wrapped_text = self._clean_and_wrap(body)

        for line in wrapped_text:
            self.pdf.multi_cell(0, 6, sanitize_text(line))

        self.pdf.ln(4)

    def add_image(self, image_path: str, width: int = 170):
        self.pdf.ln(4)
        self.pdf.image(image_path, w=width)
        self.pdf.ln(6)

    def add_reasoning_log(self, reasoning_steps):
        self.pdf.ln(6)
        self.pdf.set_font("Arial", "B", 13)
        self.pdf.multi_cell(0, 8, "System Reasoning Log")
        self.pdf.ln(3)

        self.pdf.set_font("Arial", "", 10)

        for step in reasoning_steps:
            self.pdf.multi_cell(0, 6, sanitize_text(f"- {step}"))

        self.pdf.ln(4)

    def save(self, path: str):
        self.pdf.output(path)

    # ----------------------------
    # Text Cleaning
    # ----------------------------

    def _clean_and_wrap(self, text: str):
        """
        Cleans markdown artifacts and wraps long text properly.
        """
        text = str(text)

        # Remove markdown artifacts
        text = text.replace("###", "")
        text = text.replace("##", "")
        text = text.replace("**", "")
        text = text.replace("#", "")
        text = text.strip()

        wrapped_lines = []
        for paragraph in text.split("\n"):
            if paragraph.strip() == "":
                wrapped_lines.append("")
            else:
                wrapped = textwrap.wrap(paragraph, width=95)
                wrapped_lines.extend(wrapped)

        return wrapped_lines

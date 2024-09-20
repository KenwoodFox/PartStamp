import logging
from PyQt5.QtWidgets import QTextEdit


class LogHandler(logging.Handler):
    def __init__(self, text_edit: QTextEdit, max_lines=25):
        super().__init__()
        self.text_edit = text_edit
        self.max_lines = max_lines

    def emit(self, record):
        log_entry = self.format(record)

        # Append the new log entry
        self.text_edit.append(log_entry)

        # Remove old lines if the total number exceeds max_lines
        text = self.text_edit.toPlainText()
        lines = text.split("\n")

        if len(lines) > self.max_lines:
            new_text = "\n".join(lines[-self.max_lines :])
            self.text_edit.setPlainText(new_text)

        # Scroll to the bottom
        self.text_edit.moveCursor(self.text_edit.textCursor().End)
        self.text_edit.ensureCursorVisible()


def setup_logging(text_edit: QTextEdit):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_handler = LogHandler(text_edit)
    log_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    logger.addHandler(log_handler)

    # Example log messages (optional)
    logger.info("Logging setup complete")

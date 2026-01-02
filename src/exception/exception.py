import sys
import traceback


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self._get_detailed_error_message(
            error_message, error_detail
        )

    @staticmethod
    def _get_detailed_error_message(error_message, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return (
            f"Error occurred in file [{file_name}] "
            f"at line [{line_number}] "
            f"with message: [{error_message}]"
        )

    def __str__(self):
        return self.error_message

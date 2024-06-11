import sys


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class SensorException(Exception): #Herer we are trying to create a custom exception class for our project. This Custom exception class is inheriting Exception super class.
    def __init__(self, error_message, error_detail:sys): #error_detail is of sys type which will be capturing all the complile time logs like line no, file name error message
        """
        :param error_message: error message in string format
        """
        super().__init__(error_message) #super is used to initialize the contructor of parent class ie; here Exception. Once Exception is feeded with the error message details our custom exception class can use that info(since inheritance) and raise the cutom exception message

        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message

from datetime import datetime
from queue import Empty


class Logger(object):
    """
    Class used to handle logging.
    Will Log to file and queue. The queue output is used for rendering in the GUI.
    If no que is specified it will log to stdout instead
    """
    def __init__(self, log_file=None, gui_queue=None):
        self.file = log_file
        self.queue = gui_queue

    @staticmethod
    def __get_log_prefix__(level):
        """
        Create prefix for log entries. Most entries will have the current date and time appended.
        The severity is added to the prefix based on log level.
        :param level: int log level, expected to be 0-8
        :return: str
        """
        result = ''
        if level <= 90:
            result += datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        if level <= 6:
            result += '[INFO]: '
        elif level == 8:
            result += '[ERROR]: '
        elif level == 7:
            result += '[WARNING]: '
        return result

    def log(self, message, level=2):
        """
        Write the log to all log targets
        :param message: str contains the log message
        :param level: int log level
        :return: None
        """
        prefix = self.__get_log_prefix__(level)
        message = prefix + message + '\n'
        if self.file is not None:
            try:
                with self.file.open("a", encoding='utf-8') as f:
                    f.write(message)
            except FileNotFoundError:
                if self.queue is not None:
                    self.queue.put(("ERROR: Can't write to log file. File not found/ and can't be created. \n", 8))
                else:
                    print("ERROR: Can't write to log file. File not found/ and can't be created.")
                raise FileNotFoundError
            except PermissionError:
                if self.queue is not None:
                    self.queue.put(("ERROR: Can't write to log file. Permission Error. \n", 8))
                else:
                    print("ERROR: Can't write to log file. Permission Error.")
                raise PermissionError
        if self.queue is not None:
            self.queue.put((message, level))
        else:
            print(message)

    def display(self, target, mode=None):
        """
        Renders a log message to the provided GUI element. Tries to set colors if mode is specified
        :param target: simplepygui gui element
        :param mode: str used to determine which gui backend is used
        :return: None
        """
        try:
            message = self.queue.get_nowait()
        except Empty:  # get_nowait() will get exception when Queue is empty
            message = None  # break from the loop if no more messages are queued up

        if message:
            target.update(message[0], append=True)
            if mode == 'tk':
                level = message[1]
                display = target.Widget
                if level >= 7:
                    log_line = display.index('end-2c').split('.')[0]  # returns line count
                    message_len = str(len(message[0]))
                    if level == 8:
                        display.tag_add("error", log_line + ".0", log_line + "." + message_len)
                        display.tag_config("error", foreground="red")
                    elif level == 7:
                        display.tag_add("warning", log_line + ".0", log_line + "." + message_len)
                        display.tag_config("warning", foreground="orange")

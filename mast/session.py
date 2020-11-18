from flask import session


class Session(object):
    error_msgs: list
    warning_msgs: list
    info_msgs: list

    def __init__(self):
        self.error_msgs = session.get('error') or []
        self.warning_msgs = session.get('warning') or []
        self.info_msgs = session.get('info') or []

    def __del__(self):
        session['error'] = self.error_msgs
        session['warning'] = self.warning_msgs
        session['info'] = self.info_msgs

    def error(self, msg: str):
        """
        Saves a new error message to be displayed.
        :param msg: Text of the message.
        """
        self.error_msgs.append(msg)

    def warning(self, msg: str):
        """
        Saves a new warning message to be displayed.
        :param msg: Text of the message.
        """
        self.warning_msgs.append(msg)

    def info(self, msg: str):
        """
        Saves a new info message to be displayed.
        :param msg: Text of the message.
        """
        self.info_msgs.append(msg)

    def pop_error_msgs(self) -> list:
        """
        Gets all error messages to be displayed and clears the list.
        :returns: List of the messages.
        """
        result = self.error_msgs
        self.error_msgs = []
        return result

    def pop_warning_msgs(self) -> list:
        """
        Gets all warning messages to be displayed and clears the list.
        :returns: List of the messages.
        """
        result = self.warning_msgs
        self.warning_msgs = []
        return result

    def pop_info_msgs(self) -> list:
        """
        Gets all info messages to be displayed and clears the list
        :returns: List of the messages.
        """
        result = self.info_msgs
        self.info_msgs = []
        return result

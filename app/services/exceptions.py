class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message="Invalid Usage", message_detail="", status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.message_detail = message_detail
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = {
            'message': self.message,
            'message_detail': self.message_detail,
            'data': dict(self.payload or ()),
        }
        return rv


class AppLogicExc(InvalidUsage):
    pass


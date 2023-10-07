class UserState:
    def __init__(self):
        self.state = 'initial'
        self.headers = None
        self.username = None
        self.headers = None
        self.password = None

    def set_login_state(self):
        self.state = 'login'

    def set_register_state(self):
        self.state = 'register'

    def set_chat_state(self, username, password, headers):
        self.state = 'chat'
        self.username = username
        self.password = password
        self.headers = headers

'''
Username class to pass object around
'''
class User():
    def __init__(self, user_nm=None, status=None):
        self.name = user_nm
        self.status = status

    def set_user_nm(self, user_nm):
        self.name = user_nm

    def set_status(self, status):
        self.status = status

    def logout(self):
        self.name = None
        self.status = 'Passive'
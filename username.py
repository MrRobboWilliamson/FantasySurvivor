'''
Username class to pass object around
'''
class User():
    def __init__(self, user_nm=None):
        self.name = user_nm

    def set_user_nm(self, user_nm):
        self.name = user_nm
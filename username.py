'''
Username class to pass object around
'''
class User():
    def __init__(self, user_nm=None, status='passive'):
        self.name = user_nm
        self.status = status

    def set_user_nm(self, user_nm):
        self.name = user_nm

    def set_status(self, status):
        valid = ['passive', 'participating']
        if status in valid:
            self.status = status
        else:
            raise Exception('Invalid status - must be "passive" or "participating"')

    def logout(self):
        self.name = None
        self.status = 'passive'

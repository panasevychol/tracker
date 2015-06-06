class TaskMaster:

    STATES = {'new': 1, 'in_progress': 2, 'done': 3}

    def __init__(self, app):
        self.app = app
        self.logger = self.app.logger

    def create_task(self, name, text, owner):
        #self.logger.info('Creating new task: ' + name + ' for ' + owner)
        self.app.database_master.create_task(name=name, text=text, owner=owner, state=self.STATES['new'])
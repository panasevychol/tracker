import logging

class TaskMaster:

    STATES = {'new': 1, 'in_progress': 2, 'done': 3}

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger('app')

    def create_task(self, name, text, owner):
        self.logger.info('Creating new task: ' + name + ' for ' + owner)
        error = self.app.database_master.create_task(name=name, text=text, owner=owner, state=self.STATES['new'])
        if error:
            self.logger.error(error)
            return error

    def get_current_user_tasks(self):
        tasks = []
        result = self.app.database_master.get_user_tasks(self.app.login_master.user)
        for task in result:
            tasks.append(task[1])
        return tasks

    def get_task_state(self, task_name):
        pass
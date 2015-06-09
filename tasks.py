import logging

class TaskMaster:

    STATES = {1: 'new', 2: 'in_progress', 3: 'done'}

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger('app')

    def create_task(self, name, text, owner):
        self.logger.info('Creating new task: ' + name + ' for ' + owner)
        error = self.app.database_master.create_task(name=name, text=text, owner=owner, state=1)
        if error:
            self.logger.error(error)
            return error

    def get_current_user_tasks(self):
        tasks = []
        result = self.app.database_master.get_user_tasks(self.app.login_master.user)
        for task in result:
            if task[-2] != 3:
                tasks.append(task[1])
        return tasks

    def get_task_state(self, task_name):
        result = self.app.database_master.get_task_record(task_name)[0][-2]
        if result:
            return self.STATES[result]

    def get_task_text(self, task_name):
        result = self.app.database_master.get_task_record(task_name)[2]
        if result:
            return result

    def close_task(self, task_name):
        task_record = self.app.database_master.get_task_record(task_name)
        error = self.app.database_master.update_task_state(task_record[0], 3)
        if error:
            return 'Error while closing task "' + task_name + '": ' + error

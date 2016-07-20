import time
import jsonpickle

class Idea(object):

    def __init__(self, num = 1, msg = ''):
        self.num = num
        self._mesg = msg
        self.time = self._get_time_now()

    def _get_time_now(self):
        month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        now = time.localtime(time.time())
        year = str(now[0])
        month = month[now[1]]
        day = str(now[2]).zfill(2)
        hour = str(now[3]).zfill(2)
        minute = str(now[4]).zfill(2)
        stamp = hour + ':' + minute + ' ' + month + ' ' + day + ' ' + year
        return stamp

    def set_mesg(self, msg):
        if self._mesg != msg:
            self._mesg = msg
            self.time = self._get_time_now()

    def get_mesg(self):
        return str(self._mesg)

class IdeaCollection(object):

    def __init__(self):
        self.count = 0
        self.ideas = []

    def new_idea(self):
        idea = Idea()
        idea.num = self.count + 1
        self._add_idea(idea)
        return self.ideas[-1]

    def _add_idea(self, idea):
        self.ideas.append(idea)
        self.count += 1

    def remove_idea(self,idea):
        self.ideas.remove(idea)

    def modify_idea(self, idea):
        for idya in self.ideas:
            if idya.num == idea.num:
                self.ideas[self.ideas.index(idya)] = idea
                break

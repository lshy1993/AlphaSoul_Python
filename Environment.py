class Environment(object):

    def __init__(self, rule, visualize=False):
        super().__init__()
        self._rule = rule
        self._visualize = visualize
        

    def reset(self):
        pass

    

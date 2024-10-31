from creature import Creature

class Enemy(Creature):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
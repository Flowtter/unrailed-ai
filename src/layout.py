class Layout:
    def __init__(self, keyboard):

        if keyboard == "azerty":
            self.up = 'Z'
            self.down = 'S'
            self.left = 'Q'
            self.right = 'D'

            self.ok = 'C'
            self.no = 'K'
            self.drop = 'L'
            self.change = 'P'
            self.random = 'O'

        else:
            self.up = 'W'
            self.down = 'S'
            self.left = 'A'
            self.right = 'D'

            self.ok = 'C'
            self.no = 'K'
            self.drop = 'L'
            self.change = 'P'
            self.random = 'O'

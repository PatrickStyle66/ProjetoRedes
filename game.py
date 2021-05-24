class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0]
        p2 = self.moves[1]

        winner = -1
        if p1 == "Pedra" and p2 == "Tesoura":
            winner = 0
        elif p1 == "Tesoura" and p2 == "Pedra":
            winner = 1
        elif p1 == "Papel" and p2 == "Pedra":
            winner = 0
        elif p1 == "Pedra" and p2 == "Papel":
            winner = 1
        elif p1 == "Tesoura" and p2 == "Papel":
            winner = 0
        elif p1 == "Papel" and p2 == "Tesoura":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
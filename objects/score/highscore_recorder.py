class HighscoreRecorder:
    def __init__(self):
        self.scores = []

    def load(self):
        try:
            f = open('objects/score/highscores.txt', 'r')
            s = list(map(int, f.read() .split()))
            self.scores = s
            f.close()
        except:
            self.scores = [0, 0, 0, 0, 0]
            f = open('objects/score/highscores.txt', 'w')
            for i in self.scores:
                f.write(str(i) + ' ')
            f.close()

    def save(self):
        f = open('objects/score/highscores.txt', 'w')
        for i in self.scores:
            f.write(str(i) + ' ')
        f.close()
         
    def update(self, a):
        for i in range(len(self.scores) - 1):
            if self.scores[i] < a & self.scores[i+1] > a:
                self.scores = self.scores[1:i+1] + [a] + self.scores[i+1:]
        if a > self.scores[len(self.scores) - 1]:
            self.scores = self.scores[1:len(self.scores)] + [a] + self.scores[len(self.scores):]

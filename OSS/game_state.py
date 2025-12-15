class GameState:
    def __init__(self, data):
        p = data["player"]
        self.health = p["health"]
        self.clue = p["clue"]
        self.escaped = p["escaped"]
        self.submitted = p["submitted"]
        self.detected = False

    def damage(self, amount):
        self.health = max(0, self.health - amount)

    def add_clue(self, amount):
        self.clue = min(100, self.clue + amount)

    def is_dead(self):
        return self.health <= 0

    def ending_type(self):
        if self.is_dead() or self.detected:
            return "bad"
        if self.escaped and self.clue == 100:
            return "hidden"
        if self.escaped:
            return "happy"
        return None

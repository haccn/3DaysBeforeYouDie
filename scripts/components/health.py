class Health():
    def __init__(self,app,hp) -> None:

        self.app = app
        self.hp = hp

        self.maxHP = hp

        self.minHP = 0

        self.lastDamage = 0

    def iframes(self,dur):
        if self.app.time_elapsed - self.lastDamage > dur:
            self.lastDamage = self.app.time_elapsed
            return False

        return True

    def increaseHealth(self,increment):
        self.maxHP += increment

    def decreaseHealth(self,increment):
        self.maxHP -= increment

    def takeDamage(self,dmg):
        self.hp -= dmg

        if self.hp <= self.minHP:
            self.hp = self.minHP

    def healHealth(self,heal):
        self.hp += heal

        if self.hp > self.maxHP:
            self.hp = self.maxHP





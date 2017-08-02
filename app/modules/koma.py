from enum import IntEnum

class Koma(IntEnum):
    empty = 0
    fu = 0x01
    kyosha = 0x02
    keima = 0x03
    gin = 0x04
    kin = 0x05
    kaku = 0x06
    hisha = 0x07
    gyoku = 0x08
    promoted_fu = 0x11
    promoted_kyosha = 0x12
    promoted_keima = 0x13
    promoted_gin = 0x14
    promoted_kaku = 0x16
    promoted_hisha = 0x17

    opponent_fu = 0x21
    opponent_kyosha = 0x22
    opponent_keima = 0x23
    opponent_gin = 0x24
    opponent_kin = 0x25
    opponent_kaku = 0x26
    opponent_hisha = 0x27
    opponent_gyoku = 0x28
    opponent_promoted_fu = 0x31
    opponent_promoted_kyosha = 0x32
    opponent_promoted_keima = 0x33
    opponent_promoted_gin = 0x34
    opponent_promoted_kaku = 0x36
    opponent_promoted_hisha = 0x37

    def is_first(self):
        if 0x01 <= self.value < 0x20:
            return True
        elif 0x20 <= self.value < 0x40:
            return False

    def is_keima(self):
        if self is Koma.keima:
            return True
        if self is Koma.opponent_keima:
            return True
        return False

    def can_promote(self):
        if self is Koma.kin or self is Koma.gyoku or self is Koma.opponent_kin or self is Koma.opponent_gyoku:
            return False
        if self.value & 0x10:
            return False
        return True

    def promote(self):
        try:
            return Koma(self.value | 0x10)
        except ValueError:
            return self

    def unpromote(self):
        try:
            return Koma(self.value & 0x2F)
        except ValueError:
            return self

    def go_enemy(self):
        if self.is_first():
            return Koma(self.value + 0x20)
        else:
            return Koma(self.value - 0x20)
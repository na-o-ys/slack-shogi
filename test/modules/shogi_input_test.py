
import unittest
from app.modules.shogi_input import ShogiInput, UserDifferentException, KomaCannotMoveException
from app.modules.shogi import Koma


class ShogiTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_shogi_input_is_initable(self):
        shogi = ShogiInput.init("channel_id", [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }
        ])
        self.assertEqual(shogi.channel_id, "channel_id")

        shogi = ShogiInput.init("channel_id", [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }
        ])
        self.assertIsNone(shogi)

        ShogiInput.clear("channel_id")
        shogi = ShogiInput.init("channel_id", [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }
        ])
        self.assertEqual(shogi.channel_id, "channel_id")

    def test_clear_for_non_exists_channnel(self):
        self.assertIsNone(ShogiInput.clear("channel_id_non_exists"))

    def test_move_method_should_work(self):
        channel_id = "test_move_method_should_work"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])

        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        self.assertEqual(shogi.board[5][2], Koma.fu)

    def test_move_method_should_raise_UserDifferentException(self):
        channel_id = "test_move_method_should_raise_UserDifferentException"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])

        with self.assertRaises(UserDifferentException):
            ShogiInput.move("76歩", channel_id, shogi.second_user.id)
        with self.assertRaises(UserDifferentException):
            ShogiInput.move("76歩", channel_id, shogi.second_user.id)

    def test_move_method_should_raise_KomaCannotMoveException(self):
        channel_id = "test_move_method_should_raise_KomaCannotMoveException"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])

        with self.assertRaises(KomaCannotMoveException):
            ShogiInput.move("75歩", channel_id, shogi.first_user.id)
        with self.assertRaises(KomaCannotMoveException):
            ShogiInput.move("34歩", channel_id, shogi.first_user.id)
        with self.assertRaises(KomaCannotMoveException):
            ShogiInput.move("15151歩", channel_id, shogi.first_user.id)
        with self.assertRaises(KomaCannotMoveException):
            ShogiInput.move("Wow, it's great.", channel_id, shogi.first_user.id)

    def test_set_any_user_validator(self):
        channel_id = "test_set_validotr"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])
        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        with self.assertRaises(UserDifferentException):
            ShogiInput.move("34歩", channel_id, shogi.first_user.id)
        ShogiInput.setAllMode(channel_id)
        ShogiInput.move("34歩", channel_id, shogi.first_user.id)

    def test_matta(self):
        channel_id = "test_matta"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])
        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        self.assertEqual(shogi.board[5][2], Koma.fu)
        ShogiInput.matta(channel_id, shogi.second_user.id)
        self.assertEqual(shogi.board[5][2], Koma.empty)
        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        self.assertEqual(shogi.board[5][2], Koma.fu)

    def test_matta_for_UserDifferentException(self):
        channel_id = "test_matta_for_UserDifferentException"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])
        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        self.assertEqual(shogi.board[5][2], Koma.fu)
        with self.assertRaises(UserDifferentException):
            ShogiInput.matta(channel_id, shogi.first_user.id)
        ShogiInput.move("34歩", channel_id, shogi.second_user.id)
        with self.assertRaises(UserDifferentException):
            ShogiInput.matta(channel_id, shogi.second_user.id)

    def test_matta_for_KomaCannotMoveException(self):
        channel_id = "test_matta_for_KomaCannotMoveException"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])
        with self.assertRaises(KomaCannotMoveException):
            ShogiInput.matta(channel_id, shogi.first_user.id)

    def test_matta_for_drop_komas(self):
        channel_id = "test_matta_for_da_komas"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])
        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        ShogiInput.move("34歩", channel_id, shogi.second_user.id)
        ShogiInput.move("22角", channel_id, shogi.first_user.id)
        ShogiInput.move("同銀", channel_id, shogi.second_user.id)
        ShogiInput.move("55角打", channel_id, shogi.first_user.id)
        ShogiInput.move("33角打", channel_id, shogi.second_user.id)
        ShogiInput.matta(channel_id, shogi.first_user.id)
        ShogiInput.matta(channel_id, shogi.second_user.id)
        ShogiInput.move("55角打", channel_id, shogi.first_user.id)
        ShogiInput.move("33角打", channel_id, shogi.second_user.id)

        self.assertEqual(shogi.board[4][4], Koma.kaku)
        self.assertEqual(shogi.board[2][6], Koma.opponent_kaku)

    def test_try_to_get_shogi_board(self):
        channel_id = "test_try_to_get_shogi_board"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }])
        ShogiInput.get_shogi_board(channel_id)

    def test_komaochi(self):
        channel_id = "test_komaochi"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }], "二枚落ち")

        self.assertEqual(shogi.board[7][1], Koma.empty)
        self.assertEqual(shogi.board[7][7], Koma.empty)

    def test_komaochi_move(self):
        channel_id = "test_komaochi_move"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }], "角落ち")

        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        ShogiInput.move("34歩", channel_id, shogi.second_user.id)
        ShogiInput.move("26歩", channel_id, shogi.first_user.id)
        ShogiInput.move("88角成", channel_id, shogi.second_user.id)

        self.assertEqual(len(shogi.second_tegoma), 0)

    def test_komaochi_matta(self):
        channel_id = "test_komaochi_matta"
        shogi = ShogiInput.init(channel_id, [{
            "id": "user1",
            "name": "user1name",
        }, {
            "id": "user2",
            "name": "user2name",
        }], "角落ち")

        ShogiInput.move("76歩", channel_id, shogi.first_user.id)
        ShogiInput.move("34歩", channel_id, shogi.second_user.id)
        ShogiInput.move("26歩", channel_id, shogi.first_user.id)
        ShogiInput.move("88角成", channel_id, shogi.second_user.id)
        ShogiInput.move("同銀", channel_id, shogi.first_user.id)
        ShogiInput.matta(channel_id, shogi.second_user.id)

        self.assertEqual(len(shogi.second_tegoma), 0)
        self.assertEqual(shogi.board[7][1], Koma.opponent_promoted_kaku)
        self.assertEqual(shogi.board[8][2], Koma.gin)

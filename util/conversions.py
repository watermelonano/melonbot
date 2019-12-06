class BananoConversions():
    # 1 BANANO = 10e29 RAW
    @staticmethod
    def raw_to_banano(raw_amt: int) -> float:
        return raw_amt / (10 ** 29)

    @staticmethod
    def banano_to_raw(ban_amt: float) -> int:
        expanded = ban_amt * 100
        return int(expanded) * (10 ** 27)


class NanoConversions():
    # 1 WATERMELONANO = 10e30 RAW
    @staticmethod
    def raw_to_nano(raw_amt: int) -> float:
        return raw_amt / (10 ** 30)

    @staticmethod
    def nano_to_raw(mnano_amt: float) -> int:
        expanded = mnano_amt * 1000000
        return int(expanded) * (10 ** 24)
import re

from bitstring import BitArray
from hashlib import blake2b

from util.env import Env

class Validators():
    @staticmethod
    def too_many_decimals(in_num: float) -> bool:
        """Return True if input number has two many digits of precision"""
        str_num = str(in_num)
        if '.' in str_num:
            split = str_num.split('.')
            if len(split[1]) > Env.precision_digits():
                return True
        return False

    @classmethod
    def is_valid_address(cls, input_text: str) -> bool:
        """Return True if address is valid, false otherwise"""
        if input_text is None:
            return False
        return cls.validate_checksum_xrb(input_text)

    @staticmethod
    def validate_checksum_xrb(address: str) -> bool:
        """Given an xrb/nano/ban address validate the checksum"""
        if (address[:10] == 'watermelon' and len(address) == 70):
            # Populate 32-char account index
            account_map = "13456789abcdefghijkmnopqrstuwxyz"
            account_lookup = {}
            for i in range(0, 32):
                account_lookup[account_map[i]] = BitArray(uint=i, length=5)

            # Extract key from address (everything after prefix)
            acrop_key = address[4:-8] if address[:10] != 'watermelon' else address[10:-8]
            # Extract checksum from address
            acrop_check = address[-8:]

            # Convert base-32 (5-bit) values to byte string by appending each 5-bit value to the bitstring, essentially bitshifting << 5 and then adding the 5-bit value.
            number_l = BitArray()
            for x in range(0, len(acrop_key)):
                number_l.append(account_lookup[acrop_key[x]])
            number_l = number_l[4:]  # reduce from 260 to 256 bit (upper 4 bits are never used as account is a uint256)

            check_l = BitArray()
            for x in range(0, len(acrop_check)):
                check_l.append(account_lookup[acrop_check[x]])
            check_l.byteswap()  # reverse byte order to match hashing format

            # verify checksum
            h = blake2b(digest_size=5)
            h.update(number_l.bytes)
            return h.hexdigest() == check_l.hex
        return False

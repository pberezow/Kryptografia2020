import random
from aes_adapter import AESAdapter, get_challenger, get_oracle, get_decoder


def inc_iv(iv):
    return (int(iv.hex(), 16) + 1).to_bytes(16, 'big')

def byte_xor(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

def adversary(oracle, challenger):
    msg1 = int(0).to_bytes(16, 'big')
    msg2 = int(1).to_bytes(16, 'big')

    ct_with_iv, _actual_msg = challenger(oracle, msg1, msg2)
    iv = ct_with_iv[0:16]
    ct = ct_with_iv[16:]

    msg = byte_xor(byte_xor(msg2, iv), inc_iv(iv))
    res = oracle(msg)
    if ct == res[16:]:
        return msg2, _actual_msg
    else:
        return msg1, _actual_msg

def challenger(oracle, msg1, msg2):
    pick = random.randint(0, 1)
    if pick == 0:
        msg = msg1
    else:
        msg = msg2
    
    ct_with_iv = oracle(msg)
    return ct_with_iv, msg

# def _adversary(key_store_path, key_store_pass, key_id):
#     msg1 = int(0).to_bytes(16, 'big')
#     msg2 = int(1).to_bytes(16, 'big')
    
#     aes = AESAdapter('CBC', key_store_path, key_store_pass, key_id)
#     challenger = get_challenger(aes)
#     oracle = get_oracle(aes)

#     ct_with_iv, actual_msg = challenger(msg1, msg2)
#     # print('Actual message selected by challenger: ', actual_msg)

#     iv = ct_with_iv[0:16]
#     ct = ct_with_iv[16:]

#     msg = byte_xor(byte_xor(msg2, iv), inc_iv(iv))
#     res = oracle(msg)
#     # print('Prepared msg: ', msg)
#     # print('Chalanger Res: ', ct, f' {len(ct)}')
#     # print('Oracle Result: ', res[16:], f' {len(res[16:])}')
#     # True if selected msg = message2, False if msg == message1
#     return ct == res[16:]


if __name__ == '__main__':
    key_store_path = './store.jck'
    key_store_pass = 'password'
    key_id = 'id1'

    aes = AESAdapter('CBC', key_store_path, key_store_pass, key_id)
    oracle = get_oracle(aes)

    all = 100000
    errors = 0
    for i in range(0, all):
        pointed, actual = adversary(oracle, challenger)
        if pointed != actual:
            errors += 1
    print(f'Correct {all - errors}/{all} runs ({(all - errors)/all * 100} %)')

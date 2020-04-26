import sys
from getpass import getpass
from aes_adapter import AESAdapter, AdapterError, get_oracle, get_challenger, get_decoder


def read_file(file_path, mode):
    """
        Process single file.
        In 'oracle' mode file represents message.
        In 'decode' mode file represents single encoded messages, first 16 bytes of every message 
            should be initialization vector.
        In 'challenge' mode file should have 2 lines with 2 messages (one msg in one line).
    """
    with open(file_path, 'rb') as file:
        msgs = file.read()

    if mode == 'oracle' or mode == 'decode':
        return msgs

    elif mode == 'challenge':
        msgs = list(filter(lambda x: x != b'', msgs.split(b'\n')))
        if len(msgs) != 2:
            print(f'In challenge mode expected 2 messages in file. Got {len(msgs)}.')
            exit(1)
        return msgs

    else:
        print('Incorrect mode, try oracle, challenge or decode')
        exit(1)

def write_file(file_path, messages):
    with open(file_path, 'wb') as file:
        if type(messages) == bytes:
            file.write(messages)
        else:
            for msg in messages:
                file.write(msg + b'\n')

def run_aes(aes_adapter, mode, message):
    if mode == 'oracle':
        oracle = get_oracle(aes_adapter)
        result = oracle(message)
        return result

    elif mode == 'challenge':
        challenge = get_challenger(aes_adapter)
        return challenge(message[0], message[1])

    elif mode == 'decode':
        decode = get_decoder(aes_adapter)
        result = decode(message)
        return result

def run():
    """
    RUN:
        python3 zad1.py <mode_of_encryption> <path_to_keystore> <key_id> <program's_mode> <file_1> ... <file_n>

    ARGS:
        mode_of_encryption - OFB, CTR or CBC
        path_to_keystore - path to keystore. Example keystore - store.jck 
            contains 3 keys with ids: id1, id2 and id3. Password to store.jck - 'password'
            keystore can be created with script `gen_key.sh` (./gen_key.sh KEYSTORE PASSWORD IDENT)
        key_id - id of key from keystore
        program's_mode - oracle, challenge or decode
    """
    # TODO: add parse_args
    try:
        produce_output_file = True
        enc_mode = sys.argv[1]
        store_path = sys.argv[2]
        key_id = sys.argv[3]
        mode = sys.argv[4]
        files = sys.argv[5:]
    except IndexError:
        print('Not enough arguments.')
        exit(1)
    # store_pass = getpass('Keystore password:')
    store_pass = 'password'

    # init aes
    try:
        aes_adapter = AESAdapter(enc_mode, store_path, store_pass, key_id)
    except AdapterError as ex:
        print('Error in AES initialization:  ', ex)
        exit(1)

    # run aes on each file
    for file in files:
        print(f"Processing file '{file}'...")

        message = read_file(file, mode)
        if mode != 'challenge':
            print(message, '\n --->')

        result = run_aes(aes_adapter, mode, message)
        
        print(result)

        if produce_output_file:
            if mode == 'oracle' or mode == 'challenge':
                write_file(file + '_enc', result)
                print(f'Output file: {file + "_enc"}')
            else:
                write_file(file + '_dec', result)
                print(f'Output file: {file + "_dec"}')


if __name__ == '__main__':
    run()

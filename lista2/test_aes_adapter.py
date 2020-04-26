from aes_adapter import AESAdapter


def test_ofb():
    aes = AESAdapter('OFB', './store.jck', 'password', 'id1')
    message = b'test_message'
    encrypted_message = aes.encrypt(message)
    assert message != encrypted_message

    decrypted_message = aes.decrypt(encrypted_message)
    assert decrypted_message == message

def test_ctr():
    aes = AESAdapter('CTR', './store.jck', 'password', 'id1')
    message = b'test_message'
    encrypted_message = aes.encrypt(message)
    assert message != encrypted_message

    decrypted_message = aes.decrypt(encrypted_message)
    assert decrypted_message == message

def test_cbc():
    aes = AESAdapter('CBC', './store.jck', 'password', 'id1')
    message = b'test_message'
    encrypted_message = aes.encrypt(message)
    assert message != encrypted_message

    decrypted_message = aes.decrypt(encrypted_message)
    assert decrypted_message == message

if __name__ == '__main__':
    try:
        test_cbc()
        print('CBC Passed.')
    except AssertionError as e:
        print('CBC Failed! ')
    
    try:
        test_ctr()
        print('CTR Passed.')
    except AssertionError as e:
        print('CTR Failed! ')
    
    try:
        test_ofb()
        print('OFB Passed.')
    except AssertionError as e:
        print('OFB Failed!')

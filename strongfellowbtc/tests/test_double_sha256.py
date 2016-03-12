
import strongfellowbtc

def test():
    actual = strongfellowbtc.double_sha256('hello')
    print actual
    expected = '9595c9df90075148eb06860365df33584b75bff782a510c6cd4883a419833d50'.decode('hex')[::-1].encode('hex')
    print expected
    assert actual == expected

# coding:utf-8

import pytest
from mapletree.helpers.signing import (Signing,
                                       DataSignError,
                                       MalformedSigendMessage,
                                       BadSignature)


@pytest.mark.parametrize('data',
                         ['string',
                          [1, 2],
                          {'x': 1}])
def test_signing(data):
    signing = Signing('secret_key')
    assert signing.unsign(signing.sign(data)) == data
    signing = Signing(b'secret_key')
    assert signing.unsign(signing.sign(data)) == data


def test_unserializable():
    signing = Signing('secret_key')
    pytest.raises(DataSignError, signing.sign, object())


def test_invalid_signed_msg():
    signing = Signing('secretkey')
    data1, data2 = {'x': 1}, [1, 2]

    signedmsg1 = signing.sign(data1)
    body1, signature1 = signing.b64decode(signedmsg1).rsplit('.', 1)

    signedmsg2 = signing.sign(data2)
    body2, signature2 = signing.b64decode(signedmsg2).rsplit('.', 1)

    pytest.raises(MalformedSigendMessage, signing.unsign, '---')
    pytest.raises(MalformedSigendMessage, signing.unsign, None)

    token = signing.b64encode(body1 + signature2)
    pytest.raises(MalformedSigendMessage, signing.unsign, token)

    token = signing.b64encode(body1 + '.' + signature2)
    pytest.raises(BadSignature, signing.unsign, token)

    signature3 = signing.create_signature('{a}')
    token = signing.b64encode('{a}.' + signature3)
    pytest.raises(MalformedSigendMessage, signing.unsign, token)

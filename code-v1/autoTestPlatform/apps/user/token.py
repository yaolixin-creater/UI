import time
import base64
import hmac


class Token():

    def __init__(self, key):
        self.key = key

    def generator(self, expire=2 * 60 * 60):
        ts_str = str(time.time() + expire)
        ts_byte = ts_str.encode("utf-8")
        sha1_tshex_str = hmac.new(self.key.encode(
            "utf-8"), ts_byte, 'sha1').hexdigest()
        token = ts_str + ':' + sha1_tshex_str
        b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
        return b64_token.decode("utf-8")

    def verify(self, token):
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(self.key.encode("utf-8"),
                        ts_str.encode('utf-8'), 'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            # token certification failed
            return False
        # token certification success
        return True


if __name__ == "__main__":

    pass
    key = "username=yanjy&password=Yjy@7890"
    # 一小时后过期
    token = Token(key).generator(5)
    print('token: {}'.format(token))
    time.sleep(6)
    print(Token(key).verify(token))

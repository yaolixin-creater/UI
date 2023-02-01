import time
import base64
import hmac


def generator(user_key, expire=2 * 60 * 60):
    token_header = 'dsf132cqwdsfsdafrewdcsveqrasc3reqsdvsdcdrdsvdx'
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    hmac_token_header = hmac.new(token_header.encode('utf-8'), ts_byte, 'sha1').hexdigest()
    sha1_tshex_str = hmac.new(user_key.encode(
        "utf-8"), ts_byte, 'sha1').hexdigest()
    user_token = '{}:{}:{}:{}'.format(ts_str, sha1_tshex_str, hmac_token_header,
                                      base64.urlsafe_b64encode(user_key.encode('utf-8')))
    b64_token = base64.urlsafe_b64encode(user_token.encode("utf-8"))
    return b64_token.decode("utf-8")


class AuthToken:

    def __init__(self, request):
        self.request = request
        self.user_token = self.request.META.get('HTTP_AUTHORIZATION')
        # print(self.request.META)
        # print(self.user_token)
        self.verify()

    def verify(self):
        try:
            token_str = base64.urlsafe_b64decode(self.user_token).decode('utf-8')
            token_list = token_str.split(':')
            if len(token_list) != 4:
                raise Exception('亲，token信息不完整，请退出后重新登陆。。。。')
            ts_str = token_list[0]
            if float(ts_str) < time.time():
                raise Exception('亲，token已失效，请退出后重新登陆。。。。。')
            known_sha1_tsstr = token_list[2]
            token_header = 'dsf132cqwdsfsdafrewdcsveqrasc3reqsdvsdcdrdsvdx'
            calc_sha1_tsstr = hmac.new(token_header.encode('utf-8')).hexdigest()
            if calc_sha1_tsstr != known_sha1_tsstr:
                print(calc_sha1_tsstr, known_sha1_tsstr)
                raise Exception('亲，token信息被串改，请退出后重新登陆。。。。')
            print('token验证通过。。。。')
        except Exception as e:
            if '亲' not in str(e):
                raise Exception('亲，token验证不通过，请退出后重新登陆。。。')
            else:
                raise Exception(str(e))


# if __name__ == "__main__":
#     pass
#     key = "username=yanjy&password=Yjy@7890"
#     token = generator(key, 30)
#     print('token: {}'.format(token))
#     # time.sleep(3)
#     # AutoToken(token)

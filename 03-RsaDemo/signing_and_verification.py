import base64
import rsa
from rsa import common


class RsaUtil:
    """RSA加密、解密、签名、验签工具类
    """
    PUBLIC_KEY = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAlXLaChDwOuh3u44LuSBG9qyEcALXDImW+offGm6Eugek3ndMfSoJ
ZxrdD+Eg9KqT7snnkljCsjajp67scH1i39l2jEsHlFfCavopCXCFTc0zcbma9LQe
mAl40l6dAhPSZ8bTUJC1ojrES65QTg0GBCZAorTZjmI29kWgFNeCqv4QaKbDVDMH
tOgI1i0vUg6hpxVXqWtSPUkPkBQcGqub2rA0dQu6c1F8ldW7kfrOEAviUCJez+qH
zMkdBp/Bi1q+Ua0epV0Knn9ksS5S6UvncfSc0qAxQ0KiiCBehBal8TLKEZj7fzVZ
nAYF5S51lcRWJ6J8GYuGYk+xZJHm3QnRVQIDAQAB
-----END RSA PUBLIC KEY-----"""  # 公钥

    PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEqgIBAAKCAQEAlXLaChDwOuh3u44LuSBG9qyEcALXDImW+offGm6Eugek3ndM
fSoJZxrdD+Eg9KqT7snnkljCsjajp67scH1i39l2jEsHlFfCavopCXCFTc0zcbma
9LQemAl40l6dAhPSZ8bTUJC1ojrES65QTg0GBCZAorTZjmI29kWgFNeCqv4QaKbD
VDMHtOgI1i0vUg6hpxVXqWtSPUkPkBQcGqub2rA0dQu6c1F8ldW7kfrOEAviUCJe
z+qHzMkdBp/Bi1q+Ua0epV0Knn9ksS5S6UvncfSc0qAxQ0KiiCBehBal8TLKEZj7
fzVZnAYF5S51lcRWJ6J8GYuGYk+xZJHm3QnRVQIDAQABAoIBAQCLwTmRDEH6dIXz
SGRCHKL/7lhy/tTnjos3gXPrHcrUxG0y9ND8gyED4CU1wku1QQbR2NHLE2IOkfX8
yyGkGD0sJAouK8PMvzy6GXHit+yQ0wH2qaD0kLPDbagk4gFlfe/WyCG4R3rzWI1U
UJAcTSWBH9x1yzVfZwxvO6CkjhVp9VwxvoTYRpF2Dah9jGKMRl+YY/cCBAUf49UN
ek4xoVgFl14BipLFx0QAYs2I+tK2rCB4EsVwiyec333y1Tak3KAdr1yPNHIMr7CY
U5hLAmpkXtH7h7VPZ38IWgDrm7p4wNRQlG0rj5vekP4/32oe+GB2Yq6l5x2ggQ+p
hI3axJKJAoGJAKZSQettOjx4dBzIhSlT4VRSWHVmaX1MbPkbUJ2A36ig+b5kxMTY
qZaUjHhj2xPzYn7psN5ih9vC4/7KNTIKpQ63P61zfgv/Y/w1Fd6IxtNy4KuVzCxR
nHCsUfE4P9I7Z4ZfxajLJepjOiPIsed88UsmpxvgiL1x7xKJL3H7xssFuSJIJcLF
r2sCeQDmB53eGxmz3K5LxKwDR7LWKdjfTe25LMRh0StyE/x8ep3D12P3/7Ab0S3E
Rvn6WfU0EEhxWw5ktsOlsHpd3OFn8ITME/TQkN5W+lO+cJSfV+E91Kh7RP5Is/0M
eQL1/T0LU7i/ZJfzO6/oNrjdPHsIK7oppKJScj8CgYh8FZZ0jDMMdlk6OCeQo7HS
dPTl8Zf2ERSj7MsCFunGJwLsFsXuji5H11/NWcJSahwrzzFTWHM/c3Eh3748LVDj
X7e0Mhvx24G+4eQE+EpN6sDPgpym2+Q483bW3j5PHF6qE72lppoM+iagF9USfVaP
2LCHzcZ2gA/65jptcYfoY8axWt5BJ7ctAnkAqUwtykwTzKa8uRMUro1Ud/7wmNkX
/1ONbZiu6xT+nPb5qiuabeoHSVHY5z59uN4Ac8MQLi2gGEvTDt0mEnMAiqkgc7q0
UdRtb4JppB3jpKrfIcyj+6W5qPSfZ1Cg9z7ccLu7m1GD7Aaf3r53rIxY2JimOQPs
W9WtAoGIOJFlD7YGFuElF8hnBko5FwC3yNuDNSfEvjA/xD8OaQQlxpK/syyhPdHi
ERel5OeGyY6gViAUhKVAOfVovJ1ywD+sxgNHLQjxgj4V2NerLinMV6qg1W/u4vMr
x9eDJvyheRbGChLay1sL2NCoy8zE9qPqnIYjpVRz8Z+LaYBdrjfp1/Su3LAK7w==
-----END RSA PRIVATE KEY-----"""  # 密钥

    # 初始化key
    def __init__(self,
                 company_pub_file=PUBLIC_KEY,
                 company_pri_file=PRIVATE_KEY):

        if company_pub_file:
            self.company_public_key = rsa.PublicKey.load_pkcs1(company_pub_file)
        if company_pri_file:
            self.company_private_key = rsa.PrivateKey.load_pkcs1(company_pri_file)

    def get_max_length(self, rsa_key, encrypt=True):
        """加密内容过长时 需要分段加密 换算每一段的长度.
            :param rsa_key: 钥匙.
            :param encrypt: 是否是加密.
        """
        blocksize = common.byte_size(rsa_key.n)
        reserve_size = 11  # 预留位为11
        if not encrypt:  # 解密时不需要考虑预留位
            reserve_size = 0
        maxlength = blocksize - reserve_size
        return maxlength

    def encrypt_by_public_key(self, message):
        """ 使用公钥加密
            :param message: 需要加密的明文
            :return: 加密后的文本
        """
        encrypt_result = b''
        max_length = self.get_max_length(self.company_public_key)
        while message:
            input = message[:max_length]
            message = message[max_length:]
            out = rsa.encrypt(input, self.company_public_key)
            encrypt_result += out
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    def decrypt_by_private_key(self, message):
        """使用私钥解密
            :param message: 需要解密的内容.
            :return: 解密后的文本
        """
        decrypt_result = b""

        max_length = self.get_max_length(self.company_private_key, False)
        decrypt_message = base64.b64decode(message)
        while decrypt_message:
            input = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out = rsa.decrypt(input, self.company_private_key)
            decrypt_result += out
        return decrypt_result

    def sign(self, message: bytes, private_key):
        """ 签名方法
            :param message:需要签名的文本
            :param private_key: 私钥
            :return: 签名信息
        """
        hash = rsa.compute_hash(message, 'SHA-1')
        signature = rsa.sign_hash(hash, private_key, 'SHA-1')
        # 将签名后的内容，转换为base64编码
        result = base64.b64encode(signature).decode()
        return result

    def verify(self, message: bytes, signature: str, public_key):
        """ 验签方法
        :param message: 需要验签的文本
        :param signature: 签名信息(base64编码)
        :return: 验签结果 - 使用的哈希的名称
        :Raises: VerificationError – 当签名与消息不匹配时。
        """
        signature = base64.b64decode(signature)
        # 将签名之前的内容进行hash处理
        try:
            rsa.verify(message, signature, public_key)
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    # 创建RSA加密实例
    rsa_cipher = RsaUtil()

    # 待加密的明文
    message = "S9e5Y6543PbKMcamo8tWABwkGfqdyMLtmermps5rENW".encode('utf8')
    print('加密前:\n%s' % message)

    # 客户端C-公钥加密
    encrypt_text = rsa_cipher.encrypt_by_public_key(message)
    print('客户端C-加密后:\n%s' % encrypt_text)

    # 客户端C-私钥签名
    signature = rsa_cipher.sign(message, rsa_cipher.company_private_key)
    print('客户端C-签名:\n%s' % signature)

    # 服务端S-公钥验签
    result = rsa_cipher.verify(message, signature, rsa_cipher.company_public_key)
    print('服务端S-验签:\n%s' % result)

    # 服务端S-解密
    decrypt_text = rsa_cipher.decrypt_by_private_key(encrypt_text)
    print('服务端S-解密后:\n%s' % decrypt_text)

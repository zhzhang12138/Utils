import rsa


def create_rsa_file():
    """
    创建公钥和密钥
    """
    f, e = rsa.newkeys(512)  # 生成公钥、私钥

    # 保存私钥
    e = e.save_pkcs1()  # 保存为 .pem 格式
    with open("private.pem", "wb") as x:
        x.write(e)

    # # 保存公钥
    f = f.save_pkcs1()  # 保存为 .pem 格式
    with open("public.pem", "wb") as x:
        x.write(f)


if __name__ == '__main__':
    create_rsa_file()

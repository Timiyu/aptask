from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64
from django.conf import settings

login_private_key = settings.LOGIN_PRIVATE_KEY


def create_rsa_key():
    """
    创建RSA密钥
    步骤说明：
    1、从 Crypto.PublicKey 包中导入 RSA，创建一个密码
    2、生成 1024/2048 位的 RSA 密钥
    3、调用 RSA 密钥实例的 exportKey 方法，传入密码、使用的 PKCS 标准以及加密方案这三个参数。
    4、将私钥写入磁盘的文件。
    5、使用方法链调用 publickey 和 exportKey 方法生成公钥，写入磁盘上的文件。
    """

    key = RSA.generate(1024)
    export_key = key.publickey().exportKey()
    encrypted_key = key.exportKey()
    with open("rsa_private.pem", "wb") as f:
        f.write(encrypted_key)
    with open("rsa_public.pem", "wb") as f:
        f.write(export_key)


def decrypt_password(password):
    confirm_password = base64.b64decode(password)
    with open(login_private_key, "r") as f:
        key = f.read()
    encrypted_key = key
    encrypted_key = RSA.import_key(encrypted_key)
    cipher_rsa2 = PKCS1_v1_5.new(encrypted_key)
    data = cipher_rsa2.decrypt(confirm_password, None)
    password = bytes.decode(data)
    return password


if __name__ == '__main__':
    create_rsa_key()

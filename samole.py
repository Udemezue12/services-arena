from werkzeug.security import generate_password_hash
salt = '8a5=)&xf73nntswfg_wl9n&t#t3k%&+j-@zxnq_$zy8!bgr#m('
password = '666555888'
hashed_password = generate_password_hash(password + salt)
print(hashed_password)

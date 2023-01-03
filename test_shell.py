from hello import Users

u = Users()
u.password = 'cat'

password_hash = u.password_hash
print(password_hash)


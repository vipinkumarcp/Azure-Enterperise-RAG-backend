from jose import jwt

SECRET_KEY = "my-super-secret-key"

payload = {
    "sub": "vipin",
    "role": "admin"
}

token = jwt.encode(
    payload,
    SECRET_KEY,
    algorithm="HS256"
)

print(token)
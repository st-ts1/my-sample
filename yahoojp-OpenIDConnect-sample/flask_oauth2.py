#!/bin/python3

from requests_oauthlib import OAuth2Session
import requests
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

# httpでテストする場合↓　
# 参考: https://stackoverflow.com/questions/27785375/testing-flask-oauthlib-locally-without-https
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
# HTTPセッションのキー
app.secret_key = 'hogehoge'

# アプリケーション登録した情報
# 参考: https://e.developer.yahoo.co.jp/dashboard/
client_id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client_secret = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

# Authorizationエンドポイント
# 参考: https://developer.yahoo.co.jp/yconnect/v2/authorization_code/authorization.html
authorization_base_url = 'https://auth.login.yahoo.co.jp/yconnect/v2/authorization'
# scopeも上記URL参照。全部入れた
scope = [ "openid", "profile",  "email", "address" ]
# Tokenエンドポイント
# 参考: https://developer.yahoo.co.jp/yconnect/v2/hybrid/token.html
token_url = 'https://auth.login.yahoo.co.jp/yconnect/v2/token'

@app.route("/login")
def login():
    """
    /loginへのアクセスはAuthorizationエンドポイントへリダイレクトする
    """
    yahoojp = OAuth2Session(client_id, redirect_uri="http://192.168.1.186:5000/callback", scope=scope)
    authorization_url, state = yahoojp.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    """
    アプリケーション登録したコールバックURL。
    Authorizationエンドポイントからリダイレクトされてくる
    """
    yahoojp = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri="http://192.168.1.186:5000/callback", scope=scope)
    # Tokenエンドポイントからtokenを取得する
    token = yahoojp.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    print("token:" +str(token) )

    # 属性取得APIを呼び出す
    # 参考: https://developer.yahoo.co.jp/yconnect/v2/userinfo.html
    headers = {'Authorization': "Bearer "+token.get("access_token", "") }
    res = requests.get("https://userinfo.yahooapis.jp/yconnect/v2/attribute", headers=headers)
    print("res.text:"+str(res.text) )
    return res.text

@app.route("/index.html")
def index():
    return "hoge"

## プログラム開始
if __name__ == "__main__":
    app.debug = True
    # 0.0.0.0でbind。つまりどこからの接続も受ける
    app.run(host='0.0.0.0')


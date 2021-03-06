# -*- coding: utf-8 -*-

import const_secret

CHANNEL_SECRET=const_secret.CHANNEL_SECRET
HASH_SEEDS=const_secret.HASH_SEEDS
GOOGLE_API_KEY=const_secret.GOOGLE_API_KEY
ChannelAccessToken=const_secret.ChannelAccessToken

MSG_FIRSTMSG="IFTTT2LINEはあなたのLINEとIFTTTをつなぎます。IFTTTに関しては https://ifttt.com/ を参照してください。\n使い方は https://github.com/MypaceEngine/ifttt-line/wiki/IFTTT-LINE-WIKI をご参照ください。\nIFTTTを介して情報を受信するにはIFTTTでレシピ作成時にあなたのLINEのMIDが必要になります。\nあなたのLINEのMIDは下記です。"
# MSG_NONREGISTRATION="IFTTTへの送信にはIFTTT MakerのKeyの登録が必要です。Keyは https://ifttt.com/maker から取得してください。\nKeyの登録には下記を送信してください。\n例) ifttt:reg:<Your Key>\n<Your Key>の部分はあなたのKeyです。"
MSG_NONREGISTRATION="呼鈴にはメッセージを送れませんが、コマンドを送ることで設定を変えられます。Dash Buttonが押された時に表示するメッセージを変更するにはdash:reg:message:コマンドを使います。\n例) dash:reg:message:<New Message>"
MSG_REGISTRATION="IFTTT MakerのKeyを登録しました。"
MSG_MAKERKEY_FAILED="ご登録いただいたIFTTT MakerのKeyが正しくありません。正しいIFTTT MakerのKeyを登録してください。\nKeyは https://ifttt.com/maker から取得できます。\nKeyの登録には下記を送信してください。\n例) ifttt:reg:Your Key\n<Your Key>の部分はあなたのKeyです。"
MSG_DASH_BTN_REQ="ようこそDash呼鈴へ。\n\nLineIDを登録しました。\n続いてDash Buttonを押してLineIDとDash Buttonの紐付けをしてください。"

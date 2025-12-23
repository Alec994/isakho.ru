#!/usr/bin/env python3
# generate_jitsi_jwt.py

import jwt
import time
import argparse
from datetime import datetime, timedelta

# Конфигурация
APP_ID = 'jitsi-clientID'
APP_SECRET = 'gJJBnj1nYVckl7W2i3oEm7tE5POOTGeZ'  # ваш секрет из Prosody
JITSI_DOMAIN = 'demo.isakho.ru'
ALGORITHM = 'HS256'  # или 'RS256' если используете RSA

def generate_jitsi_token(
    room_name='*',
    user_name='User',
    user_email='user@example.com',
    expires_hours=24,
    audience=None,
    issuer=None
):
    """
    Генерирует JWT токен для Jitsi Meet
    
    Args:
        room_name: название комнаты (или '*' для любой комнаты)
        user_name: имя пользователя
        user_email: email пользователя
        expires_hours: срок действия токена в часах
        audience: аудитория (по умолчанию APP_ID)
        issuer: издатель (по умолчанию APP_ID)
    """
    
    # Настройки
    aud = audience or APP_ID
    iss = issuer or APP_ID
    exp = int(time.time()) + (expires_hours * 3600)
    
    # Payload в формате Jitsi
    payload = {
        'aud': aud,                 # Аудитория
        'iss': iss,                 # Издатель
        'sub': JITSI_DOMAIN,        # Субъект (домен)
        'room': room_name,          # Комната
        'exp': exp,                 # Время истечения
        'context': {                # Контекст пользователя
            'user': {
                'name': user_name,
                'email': user_email
            }
        }
    }
    
    # Генерация токена
    token = jwt.encode(
        payload, 
        APP_SECRET, 
        algorithm=ALGORITHM
    )
    
    return token, payload

def print_token_info(token, payload):
    """Выводит информацию о токене"""
    print("\n" + "="*60)
    print("JITSI JWT TOKEN GENERATED")
    print("="*60)
    
    print("\n📋 PAYLOAD:")
    for key, value in payload.items():
        if key == 'exp':
            exp_time = datetime.fromtimestamp(value)
            print(f"  {key}: {value} ({exp_time})")
        else:
            print(f"  {key}: {value}")
    
    print(f"\n🔑 TOKEN (length: {len(token)} chars):")
    print(token)
    
    print(f"\n🌐 JOIN URL:")
    room = payload['room']
    if room == '*':
        room = 'anyroom'  # для URL нужна конкретная комната
    print(f"https://{JITSI_DOMAIN}/{room}?jwt={token}")
    
    print(f"\n📁 DIRECT LINK:")
    print(f'<a href="https://{JITSI_DOMAIN}/{room}?jwt={token}">Join {room}</a>')
    
    print("\n" + "="*60)

def decode_and_verify(token, secret=None):
    """Декодирует и проверяет токен"""
    try:
        secret = secret or APP_SECRET
        decoded = jwt.decode(
            token, 
            secret, 
            algorithms=[ALGORITHM],
            audience=APP_ID,
            issuer=APP_ID
        )
        print("✅ Token is VALID")
        return decoded
    except jwt.ExpiredSignatureError:
        print("❌ Token EXPIRED")
    except jwt.InvalidTokenError as e:
        print(f"❌ Invalid token: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description='Generate Jitsi JWT tokens')
    parser.add_argument('--room', '-r', default='testroom', help='Room name (default: testroom)')
    parser.add_argument('--name', '-n', default='User', help='User name (default: User)')
    parser.add_argument('--email', '-e', default='user@example.com', help='User email (default: user@example.com)')
    parser.add_argument('--hours', '-H', type=int, default=24, help='Token validity in hours (default: 24)')
    parser.add_argument('--audience', '-a', help='Audience claim (default: jitsi-clientID)')
    parser.add_argument('--issuer', '-i', help='Issuer claim (default: jitsi-clientID)')
    parser.add_argument('--verify', '-v', metavar='TOKEN', help='Verify an existing token')
    parser.add_argument('--secret', '-s', help='Secret key for verification')
    
    args = parser.parse_args()
    
    if args.verify:
        # Режим проверки токена
        print(f"🔍 Verifying token: {args.verify[:50]}...")
        decoded = decode_and_verify(args.verify, args.secret)
        if decoded:
            print("\nDecoded payload:")
            for key, value in decoded.items():
                print(f"  {key}: {value}")
    else:
        # Режим генерации токена
        token, payload = generate_jitsi_token(
            room_name=args.room,
            user_name=args.name,
            user_email=args.email,
            expires_hours=args.hours,
            audience=args.audience,
            issuer=args.issuer
        )
        
        print_token_info(token, payload)
        
        # Сохранить в файл
        with open('jitsi_token.txt', 'w') as f:
            f.write(f"Token: {token}\n")
            f.write(f"URL: https://{JITSI_DOMAIN}/{args.room}?jwt={token}\n")
            f.write(f"Expires: {datetime.fromtimestamp(payload['exp'])}\n")
        print("\n💾 Token saved to 'jitsi_token.txt'")


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificacion de seguridad - Argon2id + TLS 1.3
Uso: python check_security.py
"""

from django.conf import settings
import os
import sys
import django
from pathlib import Path

# Configurar Django PRIMERO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Importar DESPUES de django.setup()


def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_section(text):
    print(f"\n{text}")
    print(f"{'-'*70}\n")


def print_ok(text):
    print(f"[OK] {text}")


def print_warn(text):
    print(f"[!] {text}")


def verify_argon2id():
    """Verifica Argon2id"""
    print_section("1. CIFRADO EN REPOSO - Argon2id + Salt")

    hashers = settings.PASSWORD_HASHERS
    print(f"Hashers configurados:")
    for i, h in enumerate(hashers, 1):
        marker = " (PRIMARY)" if 'Argon2' in h else ""
        print(f"  {i}. {h}{marker}")

    if 'Argon2PasswordHasher' in hashers[0]:
        print_ok("Argon2id es el hasher primario")
    else:
        print_warn("Argon2id NO es el hasher primario")


def verify_env_vars():
    """Verifica variables de entorno"""
    print_section("2. GESTION DE LLAVES - Sin Hardcoding")

    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        print_ok(f"Archivo .env encontrado")
        with open(env_path) as f:
            lines = f.read()
            if 'SECRET_KEY' in lines:
                print_ok("SECRET_KEY cargado desde .env")
            if 'ARGON2' in lines:
                print_ok("Parametros Argon2 en .env")
    else:
        print_warn(f".env no encontrado: {env_path}")

    gitignore_path = Path(__file__).parent.parent / '.gitignore'
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            if '.env' in f.read():
                print_ok(".env protegido en .gitignore")


def verify_tls():
    """Verifica TLS 1.3"""
    print_section("3. SEGURIDAD EN TRANSITO - TLS 1.3")

    nginx_path = Path(__file__).parent.parent / 'nginx.conf'
    if nginx_path.exists():
        with open(nginx_path) as f:
            content = f.read()
            if 'TLSv1.3' in content:
                print_ok("TLS 1.3 configurado")
            if 'HSTS' in content:
                print_ok("HSTS header configurado")
    else:
        print_warn(f"nginx.conf no encontrado: {nginx_path}")


def verify_database():
    """Verifica hashes en BD"""
    from api.models import EncargadoInventario

    users = EncargadoInventario.objects.all()
    print(f"Total de encargados: {users.count()}\n")

    for user in users:
        if user.password:
            if user.password.startswith('argon2'):
                print_ok(f"{user.nombre_completo}: Hash Argon2id")
            else:
                print_warn(f"{user.nombre_completo}: Hash no es Argon2id")
        else:
            print_warn(f"{user.nombre_completo}: Sin contrasena")


def main():
    print_header("REPORTE DE SEGURIDAD - Sistema de Inventario")

    verify_argon2id()
    verify_env_vars()
    verify_tls()
    verify_database()

    print_header("VERIFICACION COMPLETADA")


if __name__ == '__main__':
    main()

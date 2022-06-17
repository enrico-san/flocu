import click
from app import application
from subprocess import call, PIPE
import os
import re
import pickledb

db = pickledb.load('~/.leo/pickle.db', True)

@click.group()
def cli():
    pass

@cli.command()
@click.option('-n', '--name', type=str, help='Special name for this key: howto, install, ...')
def key(name):
    key = f'@leo@{application.generate_key()}'
    if name:
        db.set(key, {"name": name})
    click.echo(f'\n  {key} (copied into clipboard)\n')

@cli.command()
@click.option('-k', '--key', type=str, help='Key to edit')
def edit(key):
    if not db.get(key):
        db.set(key, {})
    else:
        call(f'typora ~/.leo/{key}.md', shell=True, stderr=PIPE)

@cli.command()
@click.option('-r', '--recursive', type=str, help='Search keys in this folder and descendants')
def ls(recursive):
    for file in next(os.walk('.'))[2]:
        for line in open(file):
            k = re.match('@leo@.{8}-.{4}-.{4}-.{4}-.{12}', line)
            if not k:
                continue
            k = k.string[:41]
            db_key = db.get(k) or {}
            if k and 'name' in db_key:
                print(f'{file} -> {db_key["name"]} ({k})')
            elif k:
                print(f'{file} -> {k}')


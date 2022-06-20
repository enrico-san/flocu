import click
from app import application
from subprocess import call, PIPE
import os
import pickledb
import pyperclip
import mimetypes

HOME = os.environ['HOME']
LEO_ROOT = 'leo-tmp'
EDITOR = 'typora'
db = pickledb.load(f'{HOME}/{LEO_ROOT}/pickle.json', True)

@click.group()
def cli():
    pass

@cli.command()
@click.option('-n', '--name', type=str, help='Special name for this key: howto, install, ...')
def key(name):
    key = f'@leo@{application.generate_key()}'
    if name:
        value = db.get(key) or {}
        value['name'] = name
        db.set(key, value)
    pyperclip.copy(key)
    click.echo(f'\n  {key} (copied into clipboard)\n')

@cli.command()
@click.option('-k', '--key', type=str, help='Key to edit')
@click.option('-n', '--name', type=str, help='Special name to edit')
def edit(key, name):
    key_clpb = pyperclip.paste()
    if not key and not name:
        if application.is_key(key_clpb):
            key = key_clpb
            click.echo('Taking key from the clipboard...')
        else:
            click.echo('Input a key (-k) or a special name (-n)')
            return
    if key and not db.get(key):
        db.set(key, {})
    if name:
        for entry in db.getall():
            d = db.get(entry)
            if 'name' in d and d['name'] == name:
                key = entry
                print(f'found key {key} for special name {name}')
                break
    call(f'{EDITOR} {HOME}/{LEO_ROOT}/{key}.md', shell=True, stderr=PIPE)

@cli.command()
@click.option('-k', '--key', type=str, help='Key to show')
@click.option('-n', '--name', type=str, help='Special name to show')
def show(key, name):
    key_clpb = pyperclip.paste()
    if not key and not name:
        if application.is_key(key_clpb):
            key = key_clpb
            click.echo('Taking key from the clipboard...')
        else:
            click.echo('Input a key (-k) or a special name (-n)')
            return
    if key and db.get(key) == False:
        click.echo('Key does not exist')
        return
    if name:
        for entry in db.getall():
            d = db.get(entry)
            if 'name' in d and d['name'] == name:
                key = entry
                break
    if name and not db.get(key):
        click.echo('Name does not exist')
        return
    with open(f'{HOME}/{LEO_ROOT}/{key}.md', 'r') as f:
        print('\n', f.read(), '\n')

@cli.command()
@click.option('-r', '--recursive', type=str, help='Search keys in this folder and descendants')
@click.option('-v', '--verbose', help='Show key value too if the line has a special name', is_flag=True)
def ls(recursive, verbose):
    for file in next(os.walk('.'))[2]:
        t1, t2 = mimetypes.guess_type(file)
        if t1 != None and not t1.startswith('text'):
            continue

        for line in open(file):
            k = application.match_key(line)
            if not k:
                continue
            k = k[:41]
            db_key = db.get(k) or {}
            if k and 'name' in db_key:
                print(f'{file} -> {db_key["name"]} {k if verbose else ""}')
            elif k:
                print(f'{file} -> {k}')


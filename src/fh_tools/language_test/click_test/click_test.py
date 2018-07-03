# -*- coding: utf-8 -*-
"""
Created on 2017/10/31
@author: MG
"""
from datetime import datetime

import click


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()


@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('--name', default='Ethan', help='name')
def hello(name):
    click.echo('Hello %s!' % name)

    @click.command()
    @click.option('--password', prompt=True)  # , hide_input=True, confirmation_prompt=True
    def input_password2(password):
        click.echo('%s password: %s' % (name, password))

    input_password2()


@click.command()
@click.argument('coordinates')
def show(coordinates):
    click.echo('coordinates: %s' % coordinates)


@click.command()
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def input_password(password):
    click.echo('password: %s' % password)


def validate_time(ctx, param, value: str):
    try:
        time_obj = None if value.strip() == "" else datetime.strptime(
        datetime.now().strftime('%Y-%m-%d ') + value, '%Y-%m-%d %H:%M:%S')
        return time_obj
    except:
        raise click.BadParameter('时间格式：HH:MM:SS')


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
def cli():
    pass


def test():
    while True:
        input_str = input("type something:")
        if input_str == "exit":
            break
        @cli.command()
        @click.option('--datetime_start', callback=validate_time, prompt="起始执行时间(HH:MM:SS)(空格为当前时刻)")
        @click.option('--datetime_end', callback=validate_time, prompt="结束执行时间(HH:MM:SS)",
                      default='9:35:00')
        @click.option('--interval', type=click.INT, prompt="执行间隔时长(秒)", default=10)
        @click.option('--side', type=click.IntRange(0, 2), prompt="执行买卖方向 0 买卖 / 1 只买 / 2 只卖", default=0)
        @click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=True, default=True,
                      prompt='确认开始执行')
        def run_auto_order(**kwargs):
            print(kwargs)
            print('function finished')

        try:
            run_auto_order(standalone_mode=False)
            print('not finished yet')
        except Exception as exp:
            print(exp)

if __name__ == '__main__':
    # show()
    # hello()
    # input_password()
    test()

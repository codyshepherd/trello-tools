import click
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import trello
import yaml

from textwrap import wrap
from typing import List


class Metric(object):

    def __init__(self,
                 name: str,
                 ):
        self.name = name
        self.dates = []

    def add_date(self, date):
        self.dates.append(date)


def compile_automation_list_data(client, board_name, list_name):

    count_data_dict = {}

    boards = client.list_boards(board_filter={'name': board_name})
    found_boards = list(filter(lambda x: x.name == board_name, boards))

    if len(found_boards) == 0:
        raise Exception("No boards found")

    board_id = found_boards[0].id
    board = client.get_board(board_id)

    lists = board.get_lists('open')
    found_lists = list(filter(lambda x: x.name == list_name, lists))

    if len(found_lists) == 0:
        raise Exception("No lists found")

    notify_list = found_lists[0]
    print(notify_list)

    for card in notify_list.list_cards_iter(card_filter='all'):
        print(card.name)
        if count_data_dict.get(card.name, None) is None:
            count_data_dict[card.name] = Metric(card.name)
        if len(card.comments) < 1:
            count_data_dict[card.name].add_date(card.card_created_date)
        else:
            for comment in card.comments:
                count_data_dict[card.name].add_date(comment['data']['text'])

    return count_data_dict


def plot_data(data, title="No Title"):

    date_format = '%Y-%m-%d %H:%M:%S'

    keys_values_static = sorted(list(data.keys()))

    x = []
    y = []

    for k in keys_values_static:
        for date in data[k].dates:
            try:
                if isinstance(date, str) and len(date) > 19:
                    date = date[:19]
                    real_date = datetime.datetime.strptime(
                                    date,
                                    date_format)
                else:
                    real_date = date
            except Exception as e:
                print(f'Caught exception: {e}')
                continue
            x.append(real_date)
            y.append('\n'.join(wrap(k.split(' ')[1], 20)))

    plt.plot([], [])
    plt.scatter(x, y)

    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter(date_format)
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.title(title)

    plt.show()


@click.command()
@click.argument('board')
@click.argument('list_name')
@click.option('-c', '--config', required=True, type=click.Path(),
        help=("This option should point to a yaml file with your trello "
              "api_key, token, and api_secret"))
@click.option('-t', '--title', required=False, type=str, default="No Title"
        help="The title of your scatterplot")
def main(board, list_name, config, title):

    with open(config, 'r') as fh:
        user_config = yaml.safe_load(fh)

    key = user_config.get('api_key', '')
    token = user_config.get('token', '')
    secret = user_config.get('api_secret', '')

    client = trello.TrelloClient(
        api_key=key,
        api_secret=secret,
        token=token,
        token_secret=secret,
    )

    data = compile_automation_list_data(client, board, list_name)

    plot_data(data, title)


if __name__ == '__main__':
    main()

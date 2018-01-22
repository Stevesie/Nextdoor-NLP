import logging
import requests

from argparse import ArgumentParser

API_URL_TEMPLATE = 'https://stevesie.com/api/v1/workers/{worker_id}/collection-results'
API_REQUEST_LIMIT = 100
API_ORDER = 'asc'

def fetch_result(token, worker_id, task_collection_id, offset=0):
    print('Fetching offset {}'.format(offset))
    url = API_URL_TEMPLATE.format(worker_id=worker_id)
    result = requests.get(url,
        headers={'Token': token},
        params={
            'taskCollectionId': task_collection_id,
            'offset': offset,
            'limit': API_REQUEST_LIMIT,
            'order': API_ORDER})
    return result.json()

def fetch_and_parse_keywords(token, worker_id, task_collection_id):
    first_page = fetch_result(token, worker_id, task_collection_id)
    all_results = first_page['results']
    total_result_count = first_page['total']

    while(len(all_results) < total_result_count):
        page = fetch_result(token, worker_id, task_collection_id, offset=len(all_results))
        all_results += page['results']

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('-t', '--token', type=str)
    parser.add_argument('-w', '--worker_id', type=str)
    parser.add_argument('-c', '--task_collection_id', type=str)
    return parser

def run_command_line():
    parser = arg_parser()
    args = vars(parser.parse_args())
    fetch_and_parse_keywords(**args)

if __name__ == '__main__':
    run_command_line()

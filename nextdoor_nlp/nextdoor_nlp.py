import os
import json
import requests
import nltk

from argparse import ArgumentParser

nltk.download('punkt')

STEVESIE_API_URL_TEMPLATE = 'https://stevesie.com/api/v1/workers/{worker_id}/collection-results'
STEVESIE_API_REQUEST_LIMIT = 100
STEVESIE_API_ORDER = 'asc'

def fetch_result(token, worker_id, task_collection_id, offset=0):
    print('Fetching offset {} from Stevesie API'.format(offset))
    url = STEVESIE_API_URL_TEMPLATE.format(worker_id=worker_id)
    result = requests.get(url,
        headers={'Token': token},
        params={
            'taskCollectionId': task_collection_id,
            'offset': offset,
            'limit': STEVESIE_API_REQUEST_LIMIT,
            'order': STEVESIE_API_ORDER})
    return result.json()

def fetch_nextdoor_stories(token, worker_id, task_collection_id, stevesie_cache_filename=None):
    if stevesie_cache_filename and os.path.isfile(stevesie_cache_filename):
        print('Using cached Stevesie results')
        with open(stevesie_cache_filename) as f:
            all_results = json.load(f)
    else:
        first_page = fetch_result(token, worker_id, task_collection_id)
        all_results = first_page['results']
        total_result_count = first_page['total']

        while(len(all_results) < total_result_count):
            page = fetch_result(token, worker_id, task_collection_id, offset=len(all_results))
            all_results += page['results']

        if stevesie_cache_filename:
            print ('Writing {result_count} to cache file {cache_filename}'.format(
                result_count=len(all_results),
                cache_filename=stevesie_cache_filename))
            with open(stevesie_cache_filename, 'w') as f:
                json.dump(all_results, f)
    return all_results

def word_counts_for_story(story):
    word_counts = {}
    subject = story.get('subject')
    sentences = [comment['body'] for comment in story.get('comments', []) if comment.get('body')]

    if (subject):
        sentences.append(subject)

    for sentence in sentences:
        for token in [t.lower() for t in nltk.word_tokenize(sentence)]:
            word_counts[token] = word_counts.get(token, 0) + 1

    return word_counts

def fetch_and_parse(token, worker_id, task_collection_id, stevesie_cache_filename=None, output_filename=None):
    nextdoor_results = fetch_nextdoor_stories(token, worker_id, task_collection_id, stevesie_cache_filename)
    all_word_counts = {}
    stories_word_counts = [word_counts_for_story(result['object']) for result in nextdoor_results]
    for word_counts in stories_word_counts:
        for word, count in word_counts.items():
            all_word_counts[word] = all_word_counts.get(word, 0) + count

    results = {
        'story_count': len(stories_word_counts),
        'word_counts': all_word_counts
    }

    if output_filename:
        with open(output_filename, 'w') as f:
            json.dump(results, f)

    print('Story Word Count Summary:')
    print(results)

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('-t', '--token', type=str)
    parser.add_argument('-w', '--worker_id', type=str)
    parser.add_argument('-c', '--task_collection_id', type=str)

    parser.add_argument('-s', '--stevesie_cache_filename', type=str, required=False)
    parser.add_argument('-o', '--output_filename', type=str, required=False)
    return parser

def run_command_line():
    parser = arg_parser()
    args = vars(parser.parse_args())
    fetch_and_parse(**args)

if __name__ == '__main__':
    run_command_line()

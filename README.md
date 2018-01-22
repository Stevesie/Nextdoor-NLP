# Nextdoor NLP

### Analyze Natural Language on Nextdoor

This project will extract word frequencies from Nextdoor via Stevesie.

*Early work in progress: meant for preview only*

## Getting Started

First, [download](https://github.com/Stevesie/Nextdoor-NLP/archive/master.zip) or clone this repo.

We highly recommend using [Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/) when working with Python.  All you should need to do is:

`pip install virtualenv`

Then to either use or develop this code, from one directory level above run these commands:

```
virtualenv nextdoor_nlp
source nextdoor_nlp/bin/activate
cd nextdoor_nlp
python setup.py install
```

## Usage

1. You will need one or more workers set up and running [Nextdoor Login & Homefeed](https://stevesie.com/apps/workflows/nextdoor-login-homefeed).

2. Navigate to your worker on Stevesie and click on the *Export* tab.  Generate an API token if you have not yet done so.

3. In the red text beginning with "curl," take note of your `token`, `worker_id` (in the URL).  The Task Collection ID is `e5d9d62e-9fe6-432d-974f-33ecd5d4b03f`.

4. Run the script with your `token` and `worker_id`:

```
python nextdoor_nlp/nextdoor_nlp.py --token <TOKEN> --worker_id <WORKER_ID> --task_collection_id e5d9d62e-9fe6-432d-974f-33ecd5d4b03f
```

5. Wait a little, the first run will take a while to download NLP models.  If you'd like to cache the results from Stevesie for subsequent runs, you can use a local cache file by adding:

```
--stevesie_cache_filename ~/Desktop/nextdoor_cache.json
```

6. The script will print results to stdout, but you can also save to disk by adding:

```
--output_filename ~/Desktop/nextdoor_output.json
```

7. Check your results, they should look something like this, giving you the count of stories your worker has extracted and the word frequencies:

```json
{
  "story_count": 332,
  "word_counts": {
    "need": 190,
    "volunteers": 5,
    "!": 1149,
    "we": 682,
    "have": 746,
    "a": 2048,
    "fantastic": 9,
    "pet": 32,
    "sitter/house": 1,
    "sitter": 7
  }
}
```

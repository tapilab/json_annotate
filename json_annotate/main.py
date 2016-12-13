# -*- coding: utf-8 -*-
"""
A command-line tool to annotate json files with classification labels.

usage: json-annotate --input <file> --output <file> --display-fields <s> --search-fields <s> --labels <s> --id-field <s> [--include-terms <s> --exclude-terms <s> --label-name <s>] [--help]

Options
  -i, --input <file>           The input json file.
  -o, --output <file>          The output json file.
  -n, --include-terms <s>      The terms to match.
  -e, --exclude-terms <s>      The terms to include.
  -d, --display-fields <s>     The fields to display (comma separated).
  -s, --search-fields <s>      The fields to search for terms.
  -l, --labels <s>             The possible labels.
  -a, --label-name <s>         The label name [default: label]
  -f, --id-field <s>           The field for the object id.


"""
from docopt import docopt
import json
import os
import random
from subprocess import call
from termcolor import colored

from . import __version__

if __name__ == '__main__':
    main()

def main():
    args = docopt(__doc__,
                  version='json-annotate version ' + __version__)
    include_terms = split_args(args, '--include-terms')
    exclude_terms = split_args(args, '--exclude-terms')
    display_fields = split_args(args, '--display-fields')
    search_fields = split_args(args, '--search-fields')
    labels = split_args(args, '--labels')
    data = read_json(args['--input'])
    id_field = args['--id-field']
    print('read %d json objects from %s' % (len(data), args['--input']))
    run(data, args['--label-name'], labels, include_terms, exclude_terms, search_fields,
        display_fields, args['--output'], id_field, seed=42)

def read_json(fname):
    ret = []
    for line in open(fname):
        ret.append(json.loads(line))
    return ret

def split_args(args, k):
    if k in args and args[k]:
        return args[k].split(',')
    else:
        return []


def display_record(record, fields):
    for f in fields:
        print('%s: %s' % (f, record[f]))


def isdigit(x):
    try:
        y = int(x)
        return True
    except:
        return False


def edit_terms(terms):
    while True:
        print('\n'.join('%d:%s' % (i, t) for i, t in enumerate(terms)))
        print('(a)dd term, or enter number to delete, or (q)uit')
        command = input('$:')
        if isdigit(command):
            n = int(command)
            terms = terms[:n] + terms[n+1:]
        elif command == 'a':
            term = input('enter term:')
            terms.append(term)
        elif command == 'q':
            return terms


def does_match(val, terms):
    """
    >>> does_match('abc', ['a'])
    True
    >>> does_match('abc', ['d'])
    False
    """
    for t in terms:
        if t.lower() in val.lower():
            return True
    return False

def get_matches(data, includes, excludes, search_fields, labeled, id_field):
    """
    >>> get_matches([{'a': 'abc'}, {'a': 'bcd'}], ['b'], ['d'], ['a'], [])
    [{'a': 'abc'}]
    """
    labeledids = set([l[id_field] for l in labeled])
    matches = []
    for d in data:
        if d[id_field] in labeledids:
            continue
        match = False
        for field in search_fields:
            if does_match(d[field], includes):
                match = True
                break
        if match:
            for field in search_fields:
                if does_match(d[field], excludes):
                    match = False
                    break
        if match:
            matches.append(d)
    return matches


def display_menu(labels, matches, labeled):
    print(colored('labeled %d. %d remain' % (len(labeled), len(matches)), 'green'))
    for i, l in enumerate(labels):
        print('%s: %s' % (colored(str(i), 'blue'), l))
    print(colored('(q)', 'blue') + 'uit,    edit ' + colored('(i)', 'blue') +
          'ncludes,    edit ' + colored('(e)', 'blue') + 'xcludes')


def run(data, label_name, labels, match_terms, dontmatch_terms, search_fields, display_fields,
        outf, id_field, seed=42):
    random.seed(seed)
    random.shuffle(data)
    out = open(outf, 'a')
    labeled = [json.loads(s) for s in open(outf)] if os.path.isfile(outf) else []
    matches = get_matches(data, match_terms, dontmatch_terms, search_fields, labeled, id_field)
    print('found %d matches' % len(matches))
    while len(matches) > 0:
        match = matches.pop()
        display_record(match, display_fields)
        display_menu(labels, matches, labeled)
        command = input(colored('$:', 'blue'))
        if isdigit(command):
            label = labels[int(command)]
            match[label_name] = label
            out.write('%s\n' % json.dumps(match))
            out.flush()
            labeled.append(match)
        elif command == 'i':
            match_terms = edit_terms(match_terms)
            matches = get_matches(data, match_terms, dontmatch_terms, search_fields, labeled, id_field)
            print('found %d matches' % len(matches))
        elif command == 'e':
            dontmatch_terms = edit_terms(dontmatch_terms)
            matches = get_matches(data, match_terms, dontmatch_terms, search_fields, labeled, id_field)
            print('found %d matches' % len(matches))
        elif command == 'q':
            return

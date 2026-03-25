import sys
from difflib import SequenceMatcher


def parse_sections(filepath):
    sections = {}
    current_title = None
    current_lines = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('## '):
                if current_title:
                    sections[current_title] = ''.join(current_lines).strip()
                current_title = line.strip()[3:].strip()
                current_lines = []
            else:
                if current_title:
                    current_lines.append(line)
    if current_title:
        sections[current_title] = ''.join(current_lines).strip()
    return sections


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def diff_souls(path1, path2):
    v1 = parse_sections(path1)
    v2 = parse_sections(path2)
    all_titles = sorted(set(list(v1.keys()) + list(v2.keys())))
    results = []
    for title in all_titles:
        in_v1 = title in v1
        in_v2 = title in v2
        if in_v1 and not in_v2:
            results.append(('GONE', title, v1[title], None))
        elif in_v2 and not in_v1:
            results.append(('NEW', title, None, v2[title]))
        else:
            sim = similarity(v1[title], v2[title])
            if sim > 0.92:
                results.append(('HELD', title, v1[title], v2[title]))
            else:
                results.append(('SHIFTED', title, v1[title], v2[title]))
    return results


def print_diff(results, path1, path2):
    sep = '=' * 50
    print('\nsoul-engine diff')
    print(sep)
    print('  v1: ' + path1)
    print('  v2: ' + path2)
    print(sep + '\n')
    for status, title, old, new in results:
        tag = ('[' + status + ']').ljust(10)
        print(tag + ' ' + title)
        if status == 'SHIFTED':
            s_old = old[:200] + ('...' if len(old) > 200 else '')
            s_new = new[:200] + ('...' if len(new) > 200 else '')
            print('\n  v1: ' + s_old)
            print('  v2: ' + s_new + '\n')
    print('\n' + sep)
    held    = sum(1 for r in results if r[0] == 'HELD')
    shifted = sum(1 for r in results if r[0] == 'SHIFTED')
    new_c   = sum(1 for r in results if r[0] == 'NEW')
    gone    = sum(1 for r in results if r[0] == 'GONE')
    print('  HELD: ' + str(held) + '   SHIFTED: ' + str(shifted) + '   NEW: ' + str(new_c) + '   GONE: ' + str(gone))
    if shifted == 0 and new_c == 0 and gone == 0:
        print('\n  Nothing changed. Either the agent is stable - or the session was a warmup.')
    elif shifted > held:
        print('\n  More shifted than held. Significant movement - or the second session was more honest.')
    else:
        print('\n  More held than shifted. The foundation is strong.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python scripts/soul_diff.py SOUL_v1.md SOUL_v2.md')
        import sys; sys.exit(1)
    results = diff_souls(sys.argv[1], sys.argv[2])
    print_diff(results, sys.argv[1], sys.argv[2])

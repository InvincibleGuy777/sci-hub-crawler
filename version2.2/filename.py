import re


def get_valid_filename(filename, name_len=128):
    # return re.sub(r'[/\\|*<>?":]', '_', filename)[:name_len]
    return re.sub(r'[^0-9A-Za-z\-,._;]', '_', filename)[:name_len]


if __name__ == '__main__':
    title = r'''Implementing Virtual Reality technology for safety training in the precast/ prestressed concrete industry. Applied Ergonomics, 90, 103286.'''
    print(get_valid_filename(title))
    print(get_valid_filename(title, 40))
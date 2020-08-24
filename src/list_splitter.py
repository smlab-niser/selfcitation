"""Used to a list into ~equal parts
"""


def split_helper(lst, length, n):
    """
    Parameters:
        - lst: list[]
            the list to be split
        - length: int
            the length of the list
        - n: int
            the number of elements in a one part
    Returns:
        - chunks or something, just put a list() around the function to get a
        list of lists
    """
    for i in range(0, length, n):
        yield lst[i : i + n]


def split(list_to_split, number_of_parts):
    """List splitter
    Parameters:
        - list_to_split: list[]
            the list to be split
        - number_of_parts: int
            the number of parts the list is to be split in
    Reutrns:
        - list[list[]]
    """
    length = len(list_to_split)
    per_part = int(length / number_of_parts)
    return list(split_helper(list_to_split, length, per_part))

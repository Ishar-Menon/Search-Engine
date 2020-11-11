import pandas


def getSnippets(filename: str):
    """ 
    Reads the CSV file

    Arguments:
    filename - CSV file to be read

    Returns:
    Snippet column from the CSV file
    """

    df = pandas.read_csv(filename)
    snippets = df['Snippet']

    return snippets

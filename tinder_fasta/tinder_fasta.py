"""Summary
"""
import click
from path import Path
from Bio import SeqIO
import re
from itertools import chain
from functools import partial
from slugify import slugify


def is_matched(pattern, sequence):
    """Summary

    Parameters
    ----------
    pattern : str
        regexp or litteral string matching
    sequence : SeqIO sequence
        sequence we want to be filtered

    Returns
    -------
    bool
        True if we keep the sequence, false otherwise
    """
    # search the pattern in the sequence decription.
    # re.search return None if the pattern isn't found
    # (None as a value of False).
    return re.search(pattern, sequence.description)


def match_sequences(pattern, sequences):
    """Summary

    Parameters
    ----------
    pattern : strs
        regexp or litteral string matching
    sequence : iterable of SeqIO sequence
        sequences we want to filter

    Yields
    ------
    SeqIO sequences :
        the filtered sequences

    """
    # Get a pattern and an iterable of sequences, return the ones that match.
    yield from filter(partial(is_matched, pattern), sequences)


def get_sequences(file):
    """Summary

    Parameters
    ----------
    file : str
        a file containing the raw sequences

    Yields
    ------
    SeqIO.SeqRecord
        the sequences parsed from file
    """
    # Get a file, return the sequence
    yield from SeqIO.parse(file, "fasta")


def get_files(user_input, glob):
    """Summary

    Parameters
    ----------
    user_input : iterable of str
        The list provided by the user. Could be files or directories.
    glob : str
        for the directories, keep only the files matching this glob

    Yields
    ------
    files
        yield the file or the files in the directory
    """
    # We get the input
    path_input = Path(user_input)
    # If it's a directory..
    if path_input.isdir:
        # We send all the files
        yield from path_input.files(glob)
    # Otherwise, we check if the file exist
    elif path_input.exists:
        # And we send it.
        yield user_input


# click help to easily build command line tools.
@click.command()
@click.option('--output', '-o', default="outputs/",
              help='output directory, will be created if needed')
@click.option('--inputs', '-i', default='.',
              type=click.Path(exists=True), multiple=True,
              help='input files or directory. If directory, apply pattern'
                   ' filter according to the glob parameter')
@click.option('--glob', '-g', default="*.fna",
              help="glob pattern : will be applied to the input folder"
                   " or/and input files")
@click.argument('patterns', type=click.File('r'))
def match(patterns,
          inputs,
          output,
          glob):
    """Summary

    Parameters
    ----------
    patterns : click.File
        the file or stream containing the patterns
    inputs : list of str
        fasta files or directories where live fasta files.
    output : str
        output directory
    glob : str
        glob filtering the inot directories.
    """

    # We get all the files. Chain get iterators and chain them.
    input_files = chain(*(get_files(user_input, glob)
                          for user_input in inputs))
    # We parse all the sequences with SeqIO
    sequences = list(chain(*map(get_sequences, input_files)))

    # We create the output directory if needed
    output_dir = Path(output)
    output_dir.makedirs_p()

    # For all the patterns...
    for pattern in patterns:
        # We get only the part after the underscore
        pattern = pattern.strip().split("_")[-1]
        # We filter the sequences with that pattern
        filtered_sequences = match_sequences(pattern, sequences)
        # We write them back in the proper file
        # slugify take a wasted string and output a "nice" formated one.
        # (for example : "*$tèst`" -> "test")
        SeqIO.write(filtered_sequences,
                    output_dir / "%s.fasta" % slugify(pattern),
                    format='fasta')


if __name__ == '__main__':
    match()

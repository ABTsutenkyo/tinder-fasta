from path import Path
from collections import namedtuple

# specialized container for the data
Sample = namedtuple('Sample', ['metadata', 'sequence'])


def filter_by_name(sample, pattern):
    """Filter the samples according to the pattern

    Parameters
    ----------
    sample : Sample
        the Sample object containing metadata and sequence.
    pattern : str
        the pattern.

    Returns
    -------
    bool
        True if the metadata match the pattern
    """
    pattern = pattern.split('_')[-1]
    return ("|%s(" % pattern in sample.metadata)


def extract_sequence(lines):
    """Summary

    Parameters
    ----------
    lines : list
        list containing all the lines of the .fna files

    Yields
    ------
    Sample
        the sample containing the pair of metadata and sequence
    """

    metadatas = lines[::2]  # metadata on even lines
    sequences = lines[1::2]  # sequences on odd line
    for metadata, sequence in zip(metadatas, sequences):
        yield Sample(metadata=metadata.strip(),
                     sequence=sequence.strip())


def join_sample(sample):
    """Once we have processed the samples, we want a line which fill the .fasta

    Parameters
    ----------
    sample : Sample
        the Sample with a par of metadata and sequence

    Returns
    -------
    str
        the two lines joined by a breakline.
    """
    return "\n".join([sample.metadata, sample.sequence])


def match(pattern_file,
          input_dir=("."),
          output_dir=("./output"),
          glob="*.fna"):
    """
    The main function : will read the .fna, the list of pattern,
    do the filter process and rewrite one file per pattern.

    Parameters
    ----------
    pattern_file : TYPE
        Description
    input_dir : str, optional
        Description
    output_dir : str, optional
        Description
    pattern_file (str)
    input_dir (str, optional)
    output_dir (str, optional)
    """
    output_dir = Path(output_dir).mkdir_p()

    with open(pattern_file) as f:
        patterns = [pattern.strip()
                    for pattern
                    in f.readlines()]
    fna_files = Path(input_dir).files(glob)
    lines = []
    for file in sorted(fna_files):
        with open(file) as f:
            lines += f.readlines()
    for pattern in patterns:
        samples = [sample
                   for sample in extract_sequence(lines)
                   if filter_by_name(sample, pattern)]

        with open(output_dir / "%s.fasta" % pattern, mode="a") as f:
            f.write('\n'.join([join_sample(sample)
                               for sample in samples]))

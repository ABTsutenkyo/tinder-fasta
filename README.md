# Tinder fasta


Take a list of fasta file and match them according some pattern.
Usage :

```bash
tinder-fasta -i inputs/ -g *.fna ICElist.txt
```

Can use the stdin instead of file pattern input:

```bash
tinder-fasta -i inputs/ -g *.fna - < ICElist.txt
```

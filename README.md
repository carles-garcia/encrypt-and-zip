# encrypt-and-zip
Python 3.7+ scripts to safely and easily encrypt, decrypt, compress and extract files.

Tools like gpg, tar and zip have many different options.

You just want to use them without having to worry that you may delete something or having to read the man pages every time.

The scripts I've written ensure that **data is never overwritten** and have only 2 options: 
- Input file 
- Output file (optional, as it is deducted if possible. If it exists, the scripts stop).

The scripts are:
- `encrypt.py`: 
    - calls gpg to encrypt symmetrically a file
    - can encrypt a directory (standalone gpg can't)
    - gpg prompts for passphrase
- `decrypt.py`: 
    - calls gpg to decrypt a gpg symmetrically encrypted file 
    - can decrypt files whether they were encrypted by the previous script or standalone gpg.
- `compress.py`: 
    - compresses a file with tar or zip
    - the extension of the output file indicates the compression algorithm
    - supports: `"zip","tar", "tar.gz", "tgz", "tar.xz", "txz", "tar.bz2", "tbz"`
    - "tgz" (tar and gzip) is used by default if the output file is not specified
- `extract.py`: 
    - extracts a compressed file with tar or unzip
    - can extract files whether they were compressed by the previous script or not.


## Install
```
sudo python3 install.py
```
This just copies the scripts and the utils directory to /usr/local/bin (that's why it requires sudo). 

You can change the destination by editing install.py.

## Examples
``` 
encrypt.py personal_info.txt
encrypt.py photos_folder/
encrypt.py personal_info.txt dir/secret.gpg

decrypt.py personal_info.gpg
decrypt.py photos_folder.gpg 

compress.py photos_folder/
compress.py asdf_folder secret.zip
compress.py big_file smaller_file.xz

extract photos_folder.tgz
extract secret.zip
extract file.gz
```
That's how simple they are.

## Tests
The test suites verify that the scripts work as expected (e.g. without overwriting any data).
You can run them with `source runtest.sh` (requires pytest in a virtual env)


## License

GNU General Public License v3

![GPLv3 Logo](https://www.gnu.org/graphics/gplv3-with-text-136x68.png "GPLv3 Logo")

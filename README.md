# Python coding challenge

## Filtertool
This repo is what resulted from my attempt at solving the python challenge.  
I must say it was a good challenge, a fun experience and a great learning opportunity.

Reaching this version of the project took me almost a week.
I worked on it for **2 or 3 hours a day for 5 days**. With the first day being mainly research and doc-reading.

## Libraries
I decided the most sensible thing was to not do everything from scratch,
so I included the [Pillow Library](https://pillow.readthedocs.io/en/stable/index.html)  to perform the imaging operations.

The rest of the work only uses the Python Standard Library.
However, a `requirements.txt` file is still included for your convenience.

## Installation
Little setup is required.

Other than having Python3 installed in your system, to ensure maximum compatibility,
I recommend navigating to the first folder of the project (where this file is located) and running:
```bash
$ python3 -m venv .
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

## Usage
This project has not been through a packaging process, so all usage must be done through invoking the `python3` command 
and using the module flag, as follows, while located at the project root.

```bash
$ python3 -m filtertool [...]
```
I shall exclude the `python3 -m` section for the rest of the document.

### Commands
To actually apply an effect to an image, you must first provide the path to that image, then you must list
the name of each filter followed by that filter's parameters. For example:
```bash
$ filtertool input.jpg rotate 45
$ filtertool input.jpg overlay python.png 0.2 0.2
```
Filters may be chained, applying all of them in order, from **left to right**, to the image first provided as input.

The following has exactly the same result as the code above.
```bash
$ filtertool input.jpg rotate 45 overlay python.png 0.2 0.2
```
Each filter's arguments, if any, are required and must be passed in the order specified.

## Filters

1. `grayscale`: decolorizes the image.
--------
2. `rotate` `X`: turns the image `X` degrees _counter-clockwise_.
--------
3. `overlay` `image_2.png` `x` `y`: applies the [Overlay](https://en.wikipedia.org/wiki/Blend_modes#:~:text=two%20example%20layers-,Overlay,-%5Bedit%5D)
algorithm to blend a .png `image2` on top of the first image, centering it at coordinates `x`, `y`.
--------
4. `memeify` `top_text` `down_text`: my added optional filter, puts a string of `top_text` on the top part of the image
and `down_text` on the lower end. The text is automatically resized to fit the image.

## Options
1. `--output` `filename.filetype`: specifies the name and file format of the new image generated to be saved.
This may be omitted, which results in a file of the same name, in the same directory,
but sufixed with the names of the applied filters.
- `-o` `filename.filetype` 
--------
2. `--display`: opens a window showing a temporal copy of the result.
- `-d`
--------
3. `--display-only`: like `--display`, but does not save the result to disk.
- `-D`
--------
Additionally, at any moment you may recall any of this by calling:
4. `--help`
- `-h`

## Testing
I included a test cases meant to check the flow of the program, which may be executed and verified by running.
```bash
$ python3 -m unittest tests/__main__.py
```
However, because this project essentially just serves as a CLI shortcut to Pillow's functionality,
this test suite does **not** try to corroborate that functionality, so no tests are run on the `_fx` functions inside
`effects.py`.
The tests **do** corroborate that the filters are being applied in correct form.

## The future
Finally, because I enjoyed this project so much, I may continue to work and improve on it in the future.
(The ability to automate and streamline the creation of memes may prove very valuable in certain Slack channels).

But this shall be done in a separate location meant for its continuation, as this version is final and officially delivered.

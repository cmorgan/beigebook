
Extracting sentiment from the Beige Book
----------------------------------------

Project exploring Beige Book sentiment using (I)Python, Pandas and Matplotlib


Install
"""""""

within a Python 3+ virtualenv execute::

    pip install -r requirements.txt

Components
""""""""""

Detail is given in each file. Quick overview:

+------------------------------+--------------------------------------------+
| Component                    | Description                                |
+==============================+============================================+
| download.py:                 | Download BeigeBook content from FED        |
+------------------------------+--------------------------------------------+
| clean.py:                    | Clean content into internal datastructure  |
+------------------------------+--------------------------------------------+
| beigebook.py:                | Parse downloaded content into BeigeBook    |
|                              | object and calculate sentiment             |
+------------------------------+--------------------------------------------+
| BeigeBook.ipynb              | Data analysis and presentation             |
+------------------------------+--------------------------------------------+
| make_serve.sh                | Make and serve the Reveal.js presentation  |
|                              | from the IPython                           |
+------------------------------+--------------------------------------------+


Working with data
"""""""""""""""""

Start an IPython shell in the project root. Then::
    
    run beigebook.py
    bbs = all_bb()

This gives you a list of all the BeigeBook objects with an associated
sentiment. This is used in the IPython notebook

Viewing the notebook
""""""""""""""""""""

View the notebook with Matplotlib graphsn displayed inline::

    IPython notebook --pylab=inline


Viewing the Presentation
""""""""""""""""""""""""

Build the Reveal.js slides with::

    ./make_serve.sh


Comment on project
""""""""""""""""""

This project was "hacked" together very quickly over a weekend, the code
quality is at a functional and extensible level. If the code were to be re-used
i would start by adding basic unit-tests and then refactoring.





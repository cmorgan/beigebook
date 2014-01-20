#ipython3 nbconvert BeigeBook.ipynb --to slides --post serve
ipython3 nbconvert BeigeBook.ipynb --to slides --stdout | ./ipy_hide.py > BeigeBook.slides.html && python -mhttp.server

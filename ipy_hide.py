#!/usr/bin/env python
 
"""
fix reveal.js slides produced from IPython notebook so that the input cell is not shown
"""
 
import sys, fileinput
 
def main(): 
    for line in fileinput.input(inplace=True):
        if '</HTML>' in line.upper():
            print("""<script type="text/javascript">
function hideElements(elements, start) {
    for (var i = 0, length=elements.length; i < length; i++) {
        if (i >= start) {
            elements[i].style.display = "none";
        }
    }
}
var input_elements = document.getElementsByClassName('input');
hideElements(input_elements, 0);
var prompt_elements = document.getElementsByClassName('prompt');
hideElements(prompt_elements, 0);
</script>
"""),
        print(line),
 
if __name__ == '__main__':
   main()
   

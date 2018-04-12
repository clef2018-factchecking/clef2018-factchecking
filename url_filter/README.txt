URL filter for the CLEF-2018 Fact Checking Lab.

Works with both Python 2 (2.5+) and Python 3.
Use the provided "is_url_bad_task1" and "is_url_bad_task2" functions to check if a URL is not good for usage in tasks 1 or 2 of the lab respectively. They expect a single parameter - the URL to test, represented as a string, and return a boolean value.

The filter checks a number of matchers against the lowercased version of an input URL string.
If all items from a single line in the matchers array are contained within the URL it is deemed as not good for usage.
For task1 the matchers array is MATCHERS_ALL, for task2 - MATCHERS_SIMPLE.

In order to handle shortened URLs, the filtering functions attempt to expand all URLs to their full form (needs active internet connectivity) and then follow the same matching procedure as above using the expanded form.

The python file contains some examples, simply run it with "python url_filter.py" and observe the output.


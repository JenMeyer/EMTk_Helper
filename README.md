EMTk Helper
============

This project offers three different scripts to help the user work with the Emotion Mining Toolkit (EMTk).
It aims at easing the data generation before the EMTk analysis, the looping of the EMTk analysis for each emotion and
the handling of the results afterwards.

Both scripts currently only work with a local MongoDB Client.  The database entries in the collection that are for
analysis need to have an '_id' field with a unique identifier for each entry and a 'text' field containing the text you
want to analyze with EMTk.

Please install the required packages with
> pip -r requirements


EMTk Input Manager
------------------

This script generates a csv file in a format that makes it possible for EMTk to analyze it. This file is generated
from a collection of a MongoDB database which the user chooses. The user also chooses the length of the file by
dictating the startpoint and endpoint of the entries as well as the name of the new file.
The resulting file will be a csv file where the entries are separated by ";". It includes a header (id;text) and is
followed by the id and the text of each entry. For this purpose it is important for the entries to have an "_id" field
(contains a unique id) and a "text" field (contains the to be analysed comment).

**How to run**

In your shell environment call this to execute it:

> ./Input_Manager.py <database> <collection> <identifier> <startpoint> <endpoint> <new_filename>

with:
* **<database>**: The name of your Mongo Database on your local client you want to use
* **<collection>**: The name of the collection in your Mongo database. The entries need to have an unique '_id' field
and a 'text' field.
* **<identifier>**: An identifier for the id. Enter one letter only. This will help to distinguish different lists from
different sources by displaying the identifier before the id.
* **<startpoint>**: The startpoint in the database where the generated data list begins. The count starts with 0.
* **<endpoint>**: The endpoint in database where the generated data list ends, all elements before endpoint are included.
* **<new_filename>**: A name for the generated file. Don't include the *.csv*. The resulting file will be named after
the pattern <new_filename>_<startpoint>_<endpoint>.csv


'Looping Multiple Emotions EMTk'-Script
---------------------------------------

This script purely exists to save the user the effort of calling EMTk six times, once for each emotion. It needs to be
executed in the shared folder in EMTk where the user's files that are to be analysed are stored.

Please be aware that this script expects a csv file which entries are separated by ';'. For easily achieving this,
use the Input Manager to generate your input.

**How to run:**

In your shell environment of EMTk run this to execute it:
> ./multipleEmotionsEMTK.bash <file>

with:
* **<file>**: the file that you want to analyse with EMTk. Do include the *.csv*.

EMTk Output Manager
-------------------

This script uses the output files of EMTk to update your database entries with the results of the emotion analysis
accordingly. The results will be stored for each entry in a field named 'emotion' which contains a dictionary where
each emotion has its own entry with <emotion>: YES/NO.
It needs to be executed in the folder where EMTk's prediction results will be stored, this will be most likely the
folder you shared with EMTk. If the folder contains other folders with the naming pattern
"classification_<filename>_<emotion>" you are in the right place to start the script.
The id of the EMTk results need to correspond to the ids of your database entries (a field named "_id") but with an
identifier leading the id. For easily achieving this, use the Input Manager to generate your input.

**How to run**

In your shell environment run this to execute it:

> ./Output_Manager.py <database> <collection> <emotion> <filename>

with:
* **<database>**: The name of your Mongo Database on your local client you want to use
* **<collection>**: The name of the collection in your Mongo database. The entries need to have an unique '_id' field
that corresponds with the id in the EMTk result files.
* **<emotion>**: The emotion you analysed the file for in EMTk. You can either choose from 'joy', 'love', 'surprise',
'anger', 'sadness' and 'fear' or if you have already analysed all six emotions with EMTk use 'all' to enter all results
at once.
* **<filename>**: The name of the csv file EMTk analysed. Don't include the *.csv*.
#!/usr/bin/env python3

import pymongo
import sys
import tqdm
import argparse


class EMTk_Input_Manager:
    """
    Generates a csv file for EMTk to analyze from database entries with an user-defined length.

    Requirements:
    The database needs to be running on a local MongoDB client.
    The database entries in your collection need to have an unique '_id' field and a 'text' field containing the text
    you want to analyze.

    :returns: A csv file with ';' seperated entries, a header (id;text) with the name <new_filename>_<start>_<end>.
    """

    def __init__(self, database: str, collection: str, identifier: str) -> None:
        """
        Initializes the Input_Manager by building the connection to your local MongoDB client.

        :param database: the name of your Mongo Database
        :param collection: the name of your collection in the database
        :param identifier: an identifier for the id. One letter only. Will help to distinguish different lists
        from different sources.
        """
        #setup of local MongoDB connection
        self.client = pymongo.MongoClient()
        self.db = self.client[database]
        self.collection = self.db[collection]
        #identifier for ids (useful if multiple lists from different sources)
        if len(identifier) == 1:
            self.identifier = identifier
        else:
            print("Identifier can only have the length of 1! Please try again.")
            sys.exit()

    def generate_data(self, start: int, end: int, newfile: str) -> None:
        """
        Generates a csv file of chosen length for EMTk with a header (id;text) and the database entries.
        The database collection entries need to have an "_id" field (contains a unique id) and a "text" field
        (contains the to be analysed comment).

        :param start: startpoint in database for generated data list, very first entry is 0
        :param end: endpoint in database for generated data list, all elements before endpoint included
        :param newfile: name for the generated file
        :return: none
        """
        #opens file
        with open(newfile + "_{}_{}.csv".format(start, end), "w") as f:
            #gets all entries in collection
            comments = self.collection.find()
            #gets list length
            comlen = self.collection.count()

            #if there are less comments than end
            end = min(end, comlen)
            #writes header necessary for emtk, no spaces allowed
            f.write("id;text\n")

            #counts through entries and writes them into file
            for i in tqdm.tqdm(range(start, end)):
                comment = comments[i]
                #gets to be analysed comment and formats it
                formatted_Text = comment["text"]
                formatted_Text = formatted_Text.replace(";", ".").replace("\n", " ").replace("\"", " ")
                #enters id and text into a file seperated with ";"
                f.write(self.identifier + "{};{}\n".format(comment["_id"], formatted_Text))


#parses arguments and calls class
parser = argparse.ArgumentParser(prog='Input Manager',
                                 description='Generates a csv file for EMTk to analyze from database entries with an '
                                             'user-defined length.')
parser.add_argument('database', type=str,
                    help="the name of your Mongo Database on your local client you want to use")
parser.add_argument('collection', type=str,
                    help="the name of the collection in your Mongo database. The entries need to have an unique "
                         "\'_id\' field and a field called \'text\'")
parser.add_argument('identifier', type=str,
                    help="An identifier for the id. Enter one letter only. Will help to distinguish different lists "
                         "from different sources.")
parser.add_argument('startpoint', type=int,
                    help="The startpoint in the database where the generated data list begins, very first entry is 0")
parser.add_argument('endpoint', type=int,
                    help='The endpoint in database where the generated data list ends, all elements before endpoint '
                         'included')
parser.add_argument('new_filename', type=str,
                    help='A name for the generated list file')
args = parser.parse_args()

i = EMTk_Input_Manager(database=args.database, collection=args.collection, identifier=args.identifier)
i.generate_data(start=args.startpoint, end=args.endpoint, newfile=args.new_filename)
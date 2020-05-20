#!/usr/bin/env python3

import pymongo
import os
import csv
import tqdm
import argparse
from bson import objectid


class EMTk_Output_Manager:
    """
    Uses the output files of EMTk to update your database entries with the emotion analysis results accordingly.
    The results will be stored for each entry in a field named 'emotion' which contains a dictionary where each emotion
    has its own entry with <emotion>: YES/NO.

    Requirements:
    The database needs to be running on a local MongoDB client.
    The id of the EMTk results need to correspond to the ids of your database entries (a field named "_id"). For easily
    achieving this use the Input Manager to generate your input.
    The program needs to be executed where the results of the EMTk analysis are stored. This is most likely the shared
    folder of EMTk.
    """

    def __init__(self, database: str, collection: str) -> None:
        """
        Initializes the Output_Manager by building a connection to your local MongoDB client.

        :param database: the name of your Mongo Database
        :param collection: the name of your collection in the database
        """
        self.client = pymongo.MongoClient()

        self.db = self.client[database]

        self.collection = self.db[collection]

        #emotions emtk is trained on
        self.emotionList = ["joy", "love", "surprise", "anger", "sadness", "fear"]

    def read_emotion(self, filename: str, emotion: str) -> None:
        """
        When given the csv file and the emotion used in the EMTk analysis , all respective database entries will be
        updated in form of a dictionary entry saved in a field "emotions".
        The ids used in the EMTk analysis should be the same as the ones in the database in a field called "_id".
        Needs to be executed in the folder where prediction results landed (most likely the shared folder for EMTk).

        :param filename: the name of the csv file EMTk analysed
        :param emotion: analysed emotion ("joy", "love", "surprise", "fear", "anger", "sadness")
        :return: none
        """

        #builds output file path in shared folder of emtk
        output_folder = "classification_" + filename + "_" + emotion
        output_file = "predictions_" + emotion + ".csv"

        file_path = os.path.join(output_folder, output_file)
        print(file_path)

        with open(file_path, 'r') as f:
            #reads file
            csvreader = csv.reader(f, delimiter=",")
            next(csvreader)

            #goes through each entry and updates the database. includes a progress bar
            for entry in tqdm.tqdm(csvreader):
                #checks if the emotion detection worked (YES/NO as result)
                if "YES" == entry[1] or "NO" == entry[1]:

                    #TODO: test auf gültige ID in Datenbank

                    #updates database entry with a dictionary containing the emotions and their result
                    self.collection.update_one({"_id": objectid.ObjectId(entry[0][1:])},
                                               {"$set": {"emotions." + emotion: entry[1] == "YES"}})
                else:
                    #writes the comments with failed emotion detection into a list
                    with open("failures_" + emotion, "a") as f:
                        f.write('{}\n'.format(str(entry)))


    def read_many(self, filename: str) -> None:
        """
        When given the csv file used in the EMTk analysis, it will loop through all six emotions EMTk analyses for and
        all respective database entries will be updated in form of a dictionary entry saved in a field "emotions".
        The ids used in the EMTk analysis should be the same as the ones in the database.
        Needs to be executed in the folder where prediction results landed (most likely the shared folder for EMTk).

        :param filename: the name of the csv file EMTk analysed
        :return: none
        """
        for emotion in self.emotionList:
            print(emotion)
            self.read_emotion(filename, emotion)


parser = argparse.ArgumentParser(prog='Output Manager',
                                 description='When given the csv file used in the EMTk analysis, it will update '
                                             'database entries with the results for the emotions.')
parser.add_argument('database', type=str,
                    help="the name of your Mongo Database on your local client you want to use")
parser.add_argument('collection', type=str,
                    help="the name of the collection in your Mongo database")
parser.add_argument('emotion', type=str, choices=['all', 'joy', 'love', 'surprise', 'anger', 'sadness', 'fear'],
                    help='The emotion you analysed for in EMTk or choose \'all\' if you analyzed all six.')
parser.add_argument('filename', type=str,
                    help="the name of the csv file EMTk analysed")
args = parser.parse_args()

o = EMTk_Output_Manager(database=args.database, collection=args.collection)

if args.emotion == "all":
    o.read_many(args.filename)
else:
    o.read_emotion(args.filename, args.emotion)
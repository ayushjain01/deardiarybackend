# -*- coding: utf-8 -*-
from transformers import pipeline
import pymongo


class DearDiary:
    def __init__(self, user, entry, date):
        self.user = user
        self.date = date
        self.entry = entry
        self.client = pymongo.MongoClient(
            "mongodb+srv://ayushganna67:U9qpqS1V3tKy0sq1@deardiary.dn8lmbn.mongodb.net/")
        self.mydb = self.client["DearDiary"]
        self.entriesCol = self.mydb["entries"]
        if self.entriesCol.find({"created_at": self.date}):
            self.entriesCol.delete_many(
                {"created_at": self.date, "email": self.user})

        self.emotion = ""
        self.emotionDistribution = {}

    def emotion_polarity(self):
        classifier = pipeline(
            "text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", return_all_scores=True)
        predict = classifier(self.entry)
        score = {}
        for i in predict[0]:
            score[i["label"]] = round(i["score"] * 100, 2)
        self.emotionDistribution = score

    def get_curves(self):
        emotions = []
        sadness_curve = []
        happiness_curve = []
        anger_curve = []
        anxiety_curve = []
        dates = []
        entries = self.entriesCol.find({"email": self.user}, {
                                       "_id": 0, "created_at": 1, "emotion": 1, "emotion_distribution": 1})
        for entry in entries:
            dates.append(entry["created_at"])
            emotions.append(entry["emotion"])
            sad_score = 0
            happy_score = 0
            anger_score = 0
            anxiety_score = 0
            for emotion, score in entry["emotion_distribution"].items():
                if emotion == "sadness":
                    sad_score += score
                elif emotion == "joy" or emotion == "love":
                    happy_score += score
                elif emotion == "anger":
                    anger_score += score
                else:
                    anxiety_score += score
            sadness_curve.append(sad_score)
            happiness_curve.append(happy_score)
            anger_curve.append(anger_score)
            anxiety_curve.append(anxiety_score)
        return dates, emotion, sadness_curve, happiness_curve, anger_curve, anxiety_curve

    def main_emotion(self):
        mainscore = 0
        for emotion, score in self.emotionDistribution.items():
            if score >= mainscore:
                self.emotion = emotion
                mainscore = score

    def insert_in_db(self):
        self.emotion_polarity()
        self.main_emotion()
        mydict = {
            "email": self.user,
            "created_at": self.date,
            "content": self.entry,
            "emotion": self.emotion,
            "emotion_distribution": self.emotionDistribution
        }
        self.entriesCol.insert_one(mydict)


def main(email, content, date):
    journal = DearDiary(email, content, date)
    journal.insert_in_db()
    dates, emotion, sadness_curve, happiness_curve, anger_curve, anxiety_curve = journal.get_curves()
    return dates, emotion, sadness_curve, happiness_curve, anger_curve, anxiety_curve

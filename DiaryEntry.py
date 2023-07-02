# -*- coding: utf-8 -*-
from transformers import pipeline
import pymongo

def main(email, content, date):
    classifier = pipeline(
        "text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", return_all_scores=True)
    predict = classifier(content)
    score = {}
    for i in predict[0]:
        score[i["label"]] = round(i["score"] * 100, 2)

    client = pymongo.MongoClient(
        "mongodb+srv://ayushganna67:U9qpqS1V3tKy0sq1@deardiary.dn8lmbn.mongodb.net/")
    mydb = client["DearDiary"]
    entriesCol = mydb["entries"]
    if entriesCol.find({"created_at": date}):
        entriesCol.delete_many(
            {"created_at": date, "email": email})
    emotion = ""
    emotionDistribution = score
    mainscore = 0
    for emotion, score in emotionDistribution.items():
        if score >= mainscore:
            emotion = emotion
            mainscore = score
    mydict = {
            "email": email,
            "created_at": date,
            "content": content,
            "emotion": emotion,
            "emotion_distribution": emotionDistribution
        }
    entriesCol.insert_one(mydict)
    emotions = []
    sadness_curve = []
    happiness_curve = []
    anger_curve = []
    anxiety_curve = []
    dates = []
    entries = entriesCol.find({"email": email}, {
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
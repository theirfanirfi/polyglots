from application.models.models import Word, LessonSchema
from flask import jsonify
import json
class SimpleSentenceLessonBuilder:
    def __init__(self, lesson):
        self.data = {}
        ls = LessonSchema()
        ls.many = False
        self.lesson = lesson
        self.data['lesson'] = ls.dump(lesson)

    def split_into_words(self):
        self.words = self.lesson.sentence.split(" ")
        return self

    def create_dropDown(self):
        dropdown = list()
        if len(self.words) > 0:
            for w in self.words:
                word = Word.query.filter_by(word=w)
                if word.count() > 0:
                    word = word.first()
                    dropdown.append({str(w): word.word_meaning if word.word_meaning is not None else None,
                                     'sound': word.audio if word.audio is not None else None,
                                     'type': word.masculine_feminine_neutral if word.masculine_feminine_neutral is not None else None})

        self.data['dropdown'] = dropdown
        return self

    def build(self):
        return self.data



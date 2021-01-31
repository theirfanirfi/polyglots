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
        dropdown = {}
        if len(self.words) > 0:
            for w in self.words:
                word = Word.query.filter_by(word=w)
                if word.count() > 0:
                    dropdown.update({str(w): word.first().word_meaning})


        self.data['dropdown'] = dropdown
        return self

    def build(self):
        return self.data



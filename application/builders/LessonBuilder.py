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
                    print(word.word_meaning+' '+word.audio)
                    dropdown.append({str(w): word.word_meaning,'sound': word.audio})

        print(dropdown)
        self.data['dropdown'] = dropdown
        return self

    def build(self):
        return self.data



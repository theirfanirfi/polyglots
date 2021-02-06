from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from application.forms.forms import WordForm, UpdateWordForm
from application.utils import save_file,save_image

class WordView(FlaskView):
	@route('/',methods=['GET','POST'])
	def words(self):
		form = WordForm()
		form.select_language.choices = Language.getLanguagesForSelectField()
		if request.method == 'POST':
			if form.validate_on_submit():
				language_id = form.select_language.data
				isSaved,image_name = save_image(form.word_image.data,'word')
				isSaved,file_name = save_file(form.audio.data,'audio')
				new_word = Word(word_name=form.word_name.data,word_mean=form.word_mean.data,word_image=image_name,audio=file_name,lan_id=language_id)
				try:
					db.session.add(new_word)
					db.session.commit()
					return redirect(url_for('WordView:words'))
				except Exception as e:
					return "There was an issue in adding the word "+str(e)
			else:
				words = Word.query.all()
				return render_template('words.html',form=form,words=words)
		else:
			words = Word.query.all()
			return render_template('words.html',form=form,words=words)

	@route('/delete_word/<int:id>')
	def delete_word(self,id):
		word_to_delete = Word.query.get_or_404(id)
		try:
			db.session.delete(word_to_delete)
			db.session.commit()
			return redirect(url_for('WordView:words'))
		except:
			return "There was an issue in deleting the word"

	@route('/update_word/<int:id>',methods=['GET','POST'])
	def update_word(self,id):
		up_word = Word.query.get_or_404(id)
		form = UpdateWordForm()
		form.select_language.choices = Language.getLanguagesForSelectField()
		if request.method == 'POST':
			if form.validate_on_submit():
				language_id = form.select_language.data
				up_word.lan_id = language_id
				isSaved,image_name = save_image(form.word_image.data,'word')
				isSaved, file_name = save_file(form.audio.data, 'audio')
				if isSaved:
					up_word.word_image = image_name
					up_word.audio = file_name
					up_word.word_name = form.word_name.data
					up_word.word_mean = form.word_mean.data
				try:
					db.session.commit()
					return redirect(url_for('WordView:words'))
				except Exception as e:
					return "There was an issue while updating the word"+str(e)
			else:
				return render_template('update_word.html',form=form,up_word=up_word)
		else:
			return render_template('update_word.html',form=form,up_word=up_word)


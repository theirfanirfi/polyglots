var sentence = "";
var translation = "";
var bottom_word_input_fields = "";

function shuffle(array) {
    return array.sort(() => Math.random() - 0.5);
}

function checkWordRepeatition(index, word) {
    var base_url = "http://127.0.0.1:5000/admin/lessons/check/" + word
    $.get(base_url, function (data) {

        $('#word' + index + " #wordtimes" + index).text(data);
    });
}

function eventKeyUp(elementKeyUp, appendTo, toBeAppended, emptyBeforeAppend = false) {
    elementKeyUp.keyup(function (event) {
        if (emptyBeforeAppend) {
            appendTo.empty();
        }

        appendTo.append(toBeAppended);

    })

}

function createWord(index, word) {
    var wordFields = "";
    var placeholder = word + ": possible meanings, separted by semicolon(;)";
    wordFields += "<div id='word" + index + "' class='row' style='margin-top:6px;border-bottom:2px solid lightblue;'>";
    wordFields += "<div class='row' style='margin:12px;'>";
    wordFields += "<div class='col-md-2'><label>Word:</label></div><div class='col-md-2'><span id='wordtimes" + index + "' class='badge badge-info' style='position:absolute;'></span>"
    wordFields += "<input style='text-align:center;' type='text'name='word[]' value=" + word + " class='form-control' readonly required/></div>";

    wordFields += "<div class='col-md-1'><Button onclick='removeWord(" + index + ");' class='btn btn-danger'><i class='fa fa-trash' ></i></Button></div></div>";

    wordFields += "<div class='row' style='margin:12px;'>";
    wordFields += "<div class='col-md-2'><label>Meanings:</label></div>";
    wordFields += "<div class='col-md-5'><input type='text' placeholder='" + placeholder + "' name='word_meaning[]' class='form-control' /></div></div>";
    wordFields += "<div class='row' style='margin:12px;'>";

    wordFields += "<div class='col-md-2'><label>Word Sound: </label></div><div class='col-md-4'> <input type='file' name='word_sound[]' class='form-control' /></div></div>";
    wordFields += "<div class='row' style='margin:12px;'>";

    wordFields += "<div class='col-md-2' ><label>Word Image</label></div><div class='col-md-4'>  <input type='file' name='word_image[]' class='form-control' /></div></div>";
    //        wordFields += "<div class='row' style='margin:12px;'>";

    //    wordFields += "<div class='col-md-1'><Button onclick='removeWord(" + index + ");' class='btn btn-danger'><i class='fa fa-trash' ></i></Button></div></div>";
    wordFields += "</div>";
    return wordFields;
}


function createTags(index, word) {
    var tag = "";
    tag += "<div id=tag" + index + " class='' style='margin:6px;float:left;'>";
    tag += "<span class='badge badge-info'>" + word + "</span>";
    tag += "</div>";
    return tag;
}

function removeWord(index) {
    $('#word' + index).remove();
}

function createImageWithBottomTextForImagesLesson() {

    var image_field = "";
    image_field += '<div class="form - group row">';
    image_field += '<label> Image </label>';
    image_field += '<input type="file" name="image[]" class="form-control" required />'
    image_field += '</div >';
    image_field += '<div class="form-group row">';
    image_field += '<label>Image Bottom Word</label>';
    image_field += '<input type="text" name="bottom_word[]" class="form-control bottom_word" required/>';
    image_field += '<div class="row four_lesson_words_display_div"></div>';
    image_field += '</div>';
    return image_field;

}

$(document).ready(function () {
    //sentence
    var sentence_field = $('#sentence');
    var wordsDiv = $('#words');

    sentence_field.keyup(function (event) {
        if (event.keyCode == 190) {
            sentence = sentence.replace(".", "");
            var words = sentence.split(" ", sentence.length);
            $.each(words, function (index, element) {
                wordsDiv.append(createWord(index, element));
                checkWordRepeatition(index, element);

            });
        } else {
            sentence = sentence_field.val();
        }
    });


    //translation

    var translation_field = $('#translation');
    var translation_tags_div = $('#translation_tags');
    var translation = "";

    translation_field.keyup(function (event) {
        if (event.keyCode == 190) {
            translation = translation.replace(".", "");
            var words = translation.split(" ", translation.length);
            words = shuffle(words);
            $.each(words, function (index, element) {
                translation_tags_div.append(createTags(index, element));
            });
        } else {
            translation = translation_field.val();
        }
    });


    //single image lesson

    var bottom_word_input_field = $('#bottom_word');
    var word_display_div = $('#singleImageLessonWordDisplayDiv');

    bottom_word_input_field.keyup(function (event) {
        word_display_div.empty();
        word_display_div.append(createWord(0, bottom_word_input_field.val()));
        checkWordRepeatition(0, bottom_word_input_field.val());

    });

    //images lesson

    var createImageFieldBtn = $('#createImageField');
    createImageFieldBtn.click(function (event) {
        $('#imagesDiv').append(createImageWithBottomTextForImagesLesson());
    });


    //four image lesson
    bottom_word_input_fields = $('.bottom_word');
    console.log(bottom_word_input_fields)
    var four_image_sentence_field = $('#four_image_sentence');

    bottom_word_input_fields.keyup(function (event) {
        sentence = $(this).val();
        var field = $(this);
        var words = sentence.split(" ", sentence.length);

        if (words.length > 0) {
            $(field).next('.row .four_lesson_words_display_div').empty();
            $.each(words, function (index, element) {
                $(field).next('.row .four_lesson_words_display_div').append(createWord(index, element));
                checkWordRepeatition(index, element);
            });
        }
    });



    four_image_sentence_field.keyup(function (event) {
        sentence = $(this).val();
        var field = $(this);
        var words = sentence.split(" ", sentence.length);

        if (words.length > 0) {
            $(field).next('.row .four_lesson_words_display_div').empty();
            $.each(words, function (index, element) {
                $(field).next('.row .four_lesson_words_display_div').append(createWord(index, element));
                checkWordRepeatition(index, element);

            });
        }
    });




});

$(document.body).on('keyup', '.bottom_word', function () {
    sentence = $(this).val();
    var field = $(this);
    var words = sentence.split(" ", sentence.length);

    if (words.length > 0) {
        $(field).next('.row .four_lesson_words_display_div').empty();
        $.each(words, function (index, element) {
            $(field).next('.row .four_lesson_words_display_div').append(createWord(index, element));
            checkWordRepeatition(index, element);

        });
    }
});
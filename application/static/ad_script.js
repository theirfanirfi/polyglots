function createCountries(countries) {
    let cc = "<option value='All'>All</option>";
    for (let i = 0; i < countries.length; i++) {
        cc += "<option value='" + countries[i].name + "'>" + countries[i].name + "</option>";
    }

    return cc;
}

function createQuestionnaireField() {
    var field = "";
    field += '<div class="form-group">';
    field += '<label>Question</label>';
    field += '<input placeholder="Question" type="text" name="questionnaire_question[]" class="form-control"/>';
    field += '</div>';


    field += '<div className="form-group">';
    field += '<label>Answer to write ? </label> ';
    field += ' <input type="checkbox" name="answer_to_write[]"/>';
    field += '</div>';

    field += '<div class="form-group">';
    field += ' <label>Question tags, separated by semicolon(;)</label>';
    field += '<input placeholder="Question tags, separated by semicolon(;)" type="text" name="questionnaire_tags[]" class="form-control"/>';
    field += '</div>';
    return field;
}

$(document).ready(function () {
    let url = "http://127.0.0.1:5000/admin/ads/get_continent_countries";
    let continent_select_field = $('#ad_continent');
    continent_select_field.change(function (event) {
        let continent_code = $(this).val();
        $.get(url + '?code=' + continent_code, function (data) {
            if (continent_code == "Global") {
                $('#countriesList').html("<option value='global'>Global</option>");
            }else {
                $('#countriesList').html(createCountries(data));
            }
        })
    });


        //questionnaire and Ad

    var add_field_btn = $('#add_ad_field')
    var ad_fields_div = $('#ad_fields_div')
    add_field_btn.click(function () {
        ad_fields_div.append(createQuestionnaireField())
    });
});
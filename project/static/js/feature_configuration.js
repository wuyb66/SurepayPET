/**
 * Created by Yunbo on 2017/11/17.
 */
$(document).ready(function() {

    $.fn.setForOLH = function(inStr) {
        if ($("#id_feature").find("option:selected").text().indexOf('nline Hierarchy') > 0) {
            $('#id_colocateMemberGroup').parents('fieldset').show();
        } else {
            $('#id_colocateMemberGroup').parents('fieldset').hide();
        }
        // $('#id_averageActiveSessionPerSubscriber').parent().parent().parent().parent().parent().parent().hide();
    };

    $(this).setForOLH();

    $('#id_feature').change(function() {
        $(this).setForOLH();
    });

    $('#id_feature').load(function() {
        $(this).setForOLH();
    });

});

/**
 * Created by Yunbo on 2017/11/24.
 */
$(document).ready(function() {
    $.fn.setTotalCounterNumber = function() {
        $('#id_totalCounterNumber').val(parseFloat($('#id_nonAppliedBucketNumber').val()) +
            parseFloat($('#id_nonAppliedUBDNumber').val()) +  parseFloat($('#id_appliedBucketNumber').val()) +
            parseFloat($('#id_appliedUBDNumber').val()));
    };

    $(this).setTotalCounterNumber();

    $('#id_nonAppliedBucketNumber').change(function() {
        $(this).setTotalCounterNumber();
    });

    $('#id_nonAppliedUBDNumber').change(function() {
        $(this).setTotalCounterNumber();
    });

    $('#id_appliedBucketNumber').change(function() {
        $(this).setTotalCounterNumber();
    });

    $('#id_appliedUBDNumber').change(function() {
        $(this).setTotalCounterNumber();
    });

});


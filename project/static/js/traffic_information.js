/**
 * Created by Yunbo on 2017/11/17.
 */
$(document).ready(function() {
    $.fn.toNumber = function(inStr) {
        var outStr = inStr.replace(/,/g, '');
        return parseFloat(outStr);
    };

    $.fn.setDiameterTrafficBHTA = function() {
        $('#id_trafficBHTA').val(parseFloat($('#id_volumeCCRiBHTA').val()) +
            parseFloat($('#id_volumeCCRuBHTA').val()) +  parseFloat($('#id_volumeCCRtBHTA').val()) +
            parseFloat($('#id_timeCCRiBHTA').val()) + parseFloat($('#id_timeCCRuBHTA').val()) +
            parseFloat($('#id_timeCCRtBHTA').val()));

        $('#id_trafficTPS').val(Math.ceil($('#id_trafficBHTA').val() * $(this).toNumber($('#id_activeSubscriber').val()) / 3600));
    };

    $.fn.setForDiameterSession = function(inStr) {
        if ($("#id_callType").find("option:selected").text().indexOf('Diameter Session') > 0) {
            $('#id_averageActiveSessionPerSubscriber').parents('fieldset').show();
            $('#id_trafficBHTA').attr("readonly","readonly");
            $('#id_trafficTPS').attr("readonly","readonly");
            $(this).setDiameterTrafficBHTA();
        } else {
            $('#id_averageActiveSessionPerSubscriber').parents('fieldset').hide();
            $('#id_trafficBHTA').removeAttr("readonly");
            $('#id_trafficTPS').removeAttr("readonly");
            $('#id_trafficBHTA').val(0);
            $('#id_trafficTPS').val(0);
        }
        // $('#id_averageActiveSessionPerSubscriber').parent().parent().parent().parent().parent().parent().hide();
    };

    $(this).setForDiameterSession();

    $('#id_callType').change(function() {
        $(this).setForDiameterSession();
    });

    $('#id_callType').load(function() {
        $(this).setForDiameterSession();
    });

    $.fn.setTrafficBHTA = function() {
        if ($(this).toNumber($('#id_activeSubscriber').val()) > 0) {
            $('#id_trafficBHTA').val(($('#id_trafficTPS').val() * 3600 / $(this).toNumber($('#id_activeSubscriber')).val()).toPrecision(4));
        }
    };

    $.fn.setTrafficTPS = function() {
        $('#id_trafficTPS').val(Math.ceil($('#id_trafficBHTA').val() * $(this).toNumber($('#id_activeSubscriber').val()) / 3600));
    };

    $('#id_volumeCCRiBHTA').change(function() {
        $(this).setDiameterTrafficBHTA();
    });

    $('#id_volumeCCRuBHTA').change(function() {
        $(this).setDiameterTrafficBHTA();
    });

    $('#id_volumeCCRtBHTA').change(function() {
        $(this).setDiameterTrafficBHTA();
    });

    $('#id_timeCCRiBHTA').change(function() {
        $(this).setDiameterTrafficBHTA();
    });

    $('#id_timeCCRuBHTA').change(function() {
        $(this).setDiameterTrafficBHTA();
    });

    $('#id_timeCCRtBHTA').change(function() {
        $(this).setDiameterTrafficBHTA();
    });

    $('#id_trafficBHTA').change(function() {
        $(this).setTrafficTPS();
    });

    $('#id_activeSubscriber').change(function() {
        $(this).setTrafficTPS();
    });

    $('#id_trafficTPS').change(function() {
        $(this).setTrafficBHTA();
    });
});

/**
 * Created by Yunbo on 2017/11/17.
 */
$(document).ready(function() {
    $('#id_applicationName').change(function(){
        var application_id = $('#id_applicationName').val();

        $.ajax({
            type: "GET",
            url: "/getotherappinformation?pk="+application_id,
            dataType:'json',
            success: function(data,textStatus){
                $('#id_activeSubscriber').val(data.ActiveSubscriber);
                $('#id_inactiveSubscriber').val(data.InactiveSubscriber);
                $('#id_trafficTPS').val(data.TrafficTPS);
            }
        })
    })

    $.fn.setForApplication = function() {
        if ($("#id_applicationName").find("option:selected").text().indexOf('DRouter') >= 0) {
            $('#id_activeSubscriber').parents('fieldset').show();
        } else {
            $('#id_activeSubscriber').parents('fieldset').hide();
        }
    };

    $(this).setForApplication();

    $('#id_applicationName').change(function() {
        $(this).setForApplication();
    });

    $('#id_applicationName').load(function() {
        $(this).setForApplication();
    });
});

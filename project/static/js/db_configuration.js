$(document).ready(function() {
    $('#id_dbInfo').change(function(){
        $(this).get_record_size();
    });

    $('#id_application').change(function(){
        $(this).get_record_size();
    });

    $('#id_memberGroupOption').change(function(){
        $(this).get_record_size();
    });

    $.fn.get_record_size = function(){
        var dbInfo_id = $('#id_dbInfo').val();
        var memberGroupOption = $('#id_memberGroupOption').val();
        var application = $('#id_application').val();

        if ((dbInfo_id != "") && (application != "")) {
            $.ajax({
                type: "GET",
                url: "/getrecordsize?pk=" + dbInfo_id + "&memberGroupOption=" + memberGroupOption + "&application=" + application,
                dataType: 'json',
                success: function (data, textStatus) {
                    var content = data.RecordSize;
                    // $.each(data, function(i, item){
                    //     content+='<option value='+item.pk+'>'+item.fields.name+'</option>'
                    // });
                    $('#id_recordSize').val(data.RecordSize);
                    $('#id_referenceDBFactor').val(data.RefDBFactor);
                    if ($('#id_dbFactor').val() <= 0) {
                        $('#id_dbFactor').val(data.RefDBFactor);
                    }

                    $('#id_subscriberNumber').val(data.SubscriberNumber);
                }
            });
        }
    };
});

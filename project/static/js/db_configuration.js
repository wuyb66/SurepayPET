$(document).ready(function() {
    $('#id_dbInfo').change(function(){
    //     var id = $('#id_dbInfo').val();
    //     $.getJSON("{% url 'select:getrecordsize' %}?pk="+id, function(data,textStatus){
    //         var content='';
    //         $.each(data, function(i, item){
    //             content+='<option value='+item.pk+'>'+item.fields.name+'</option>'
    //         });
    //         $('#id_recordSize').val(content)
    //     });
    // });
    // function getRecordSize(dbInfo_id){
        var dbInfo_id = $('#id_dbInfo').val();
        var memberGroupOption = $('#id_memberGroupOption').val();

        $.ajax({
            type: "GET",
            url: "/getrecordsize?pk="+dbInfo_id+"&memberGroupOption="+memberGroupOption,
            dataType:'json',
            success: function(data,textStatus){
                var content=data.RecordSize;
                // $.each(data, function(i, item){
                //     content+='<option value='+item.pk+'>'+item.fields.name+'</option>'
                // });
                $('#id_recordSize').val(data.RecordSize);
                $('#id_dbFactor').val(data.RefDBFactor);
                $('#id_subscriberNumber').val(data.SubscriberNumber);

                //         $('#id_recordSize').val(content)
                // var citySelect = document.getElementById("id_city");
                // for ( var i=citySelect.options.length-1; i>-1; i--){
                //     citySelect[i] = null;
                // }
                // if(data.length > 0) {
                //     $("#id_city").show();
                //     for(i=0;i<data.length;i++){
                //         citySelect.options[i] = new Option();
                //         citySelect.options[i].text = data[i].label;
                //         citySelect.options[i].value = data[i].text;
                //     }
                // }else
                //     $("#id_city").hide();
            }
        })
    })
});

/**
 * Created by Yunbo on 2017/10/16.
 */
$('#id_province').change(function(){
    var id = $('#id_province').val();
    $.getJSON("{% url 'getdata' %}?pk="+id, function(data,textStatus){
        var content='';
        $.each(data, function(i, item){
            content+='<option value='+item.pk+'>'+item.fields.name+'</option>'
        });
        $('#id_city').html(content)
    });
});

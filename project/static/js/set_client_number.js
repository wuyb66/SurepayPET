/**
 * Created by Yunbo on 2017/11/13.
 */
$(document).ready(function(){
    $('#id_cpuNumber').change(function() {
        var selectval = $('#id_cpuNumber').val();
        var options = $("#id_cpuNumber option:selected");
        var selected = options.text();
        $('#id_clientNumber').val(Math.ceil(selected / 2));
        // $('#id_clientNumber').val(Math.ceil($("select[@name=id_cpuNumber] option[@selected]").text())))
    });
});
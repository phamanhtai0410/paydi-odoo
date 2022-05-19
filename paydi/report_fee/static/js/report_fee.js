
odoo.define('sample_webcontrol.script', function (require) {

    "use strict";

var ajax = require('web.ajax');
$(document).ready(function() {
    $('.s_website_form').on('click','#submit',function(){

    var from = $('#fromdate').val();
    var to = $('#todate').val();

ajax.jsonRpc("/json_call_fun", 'call',{

  fromdate : from,

  todate : to,


}).then(function(result){ 

    });
})
})
});




odoo.define('exportfee.script', function (require) {

    "use strict";

    var ajax = require('web.ajax');
    $(document).ready(function () {
        $('.s_website_form').on('click', '#submit', function () {

            var from = $('#fromdate').val();
            var to = $('#todate').val();
            var crr_url = window.location.href ;
    
            const indexOfFirst = crr_url.search('&id=');
            const indexOfEnd = crr_url.search('&menu_id');
            const ids = crr_url.slice(indexOfFirst+4, indexOfEnd)
        
            ajax.jsonRpc("/exportfee", 'call', {
                crr_url: crr_url,
                fromdate: from,
                todate: to,

            }).then(function (result) {
                console.log('func reload in js')
                location.reload(true);
            });
            return;
        })
    })
});



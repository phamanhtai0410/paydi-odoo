
odoo.define('forcontrol.script', function (require) {

    "use strict";

    var ajax = require('web.ajax');
    $(document).ready(function () {
        $('.forcontrol').on('click', function () {

            var crr_url = window.location.href ;
        
            ajax.jsonRpc("/forcontrol", 'call', {
                crr_url: crr_url,


            }).then(function (result) {
                const path = result.url
                window.location.href=path;
                console.log("clicked",path)

            });
            return;
        })
    })
});



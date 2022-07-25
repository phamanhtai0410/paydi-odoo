
// odoo.define('exportfee.script',['web.ajax','web.FormController'], function (require) {


    odoo.define('exportfee.script',['web.ajax','web.FormController'], function (require) {

        "use strict";
    
        var ajax = require('web.ajax');
        console.log('hello, let begin')
    
        var FormController = require('web.FormController');
    
        function myfunction(){
            var from = $('#fromdate').val();
            var to = $('#todate').val();
            if(!from && !to){
                alert(' nhap time')
            }else {
                var crr_url = window.location.href ;

            const indexOfFirst = crr_url.search('&id=');
            const indexOfEnd = crr_url.search('&menu_id');
            const ids = crr_url.slice(indexOfFirst+4, indexOfEnd)
        
            ajax.jsonRpc("/exportfee", 'call', {
                crr_url: crr_url,
                fromdate: from,
                todate: to,

            }).then(function (result) {
                const path = result.url
                console.log('path--------------', path)
                if (path !== false) {
                    if(path == 'not_value') {
                        alert("Vui lòng nhập đủ thông tin phí máy");
                    }
                    else {
                        window.open(path, '_blank');
                        location.reload(true);
                    }
                }
                else {
                    alert("Vui lòng nhập phí máy");
                }
            });
                return;
            }
        }
    
        var reportController = FormController.include({
            
            _onButtonClicked: function (event) {
                console.log(event)
                console.log(event.data.attrs.id )
                
                if(event.data.attrs.id === "submit_fee"){
                    // your code
                    myfunction()
                }
                this._super(event);
            },
        });
        return reportController
    });


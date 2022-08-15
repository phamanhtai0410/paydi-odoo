/** @odoo-module **/
import AbstractField from 'web.AbstractField';
import fieldRegistry from 'web.field_registry';
import core from 'web.core';

var _t = core._t;
var QRWidget = AbstractField.extend({
    className: 'o_qr_widget',
    template: "QrWidget",
    start: function(){
        this._super.apply(this, arguments);
        if (this.recordData[this.nodeOptions.currentValue]){
            this.value = this.recordData[this.nodeOptions.currentValue]
        }
    },
    _render: function() {
        var self = this;
        var value = this.value;
        
        let qrcodearray = value.split('-')
        console.log(qrcodearray)
       
        let qrcodeimg = dynamicQrcode(qrcodearray[0],qrcodearray[1],qrcodearray[2],qrcodearray[3],'',"TT "+ qrcodearray[4]+" cua Bean Bakery")
        this.$('.qrcode_holder').html(qrcodeimg);
        // this.$('.progress-bar-inner').css('width', widthComplete + '%');
    },
})
fieldRegistry.add('qrcode', QRWidget);

var UrlImage = AbstractField.extend({
    className: 'o_attachment_image',
    template: 'FieldImageURL',
    placeholder: "/web/static/src/img/placeholder.png",
    supportedFieldTypes: ['char'],

    url: function () {
        return this.value ? this.value : this.placeholder;
    },

    _render: function () {
        this._super(arguments);

        var self = this;
        var $img = this.$("img:first");
        $img.on('error', function () {
            $img.attr('src', self.placeholder);
            self.do_warn(
                _t("Image"), _t("Could not display the selected image."));
        });
    },
});

fieldRegistry.add('image_url', UrlImage);

// odoo.define('mid', function (require) {
//     "use strict";
//     $(document).ready(function () {
//
//         //submitForm();
//         alert("de");
//         $("body ").on("click", ".mid_view #click_me", function (ev) {
//
//
//             getAllMidTemplate();
//         });
//
//         function getContactId() {
//             var fullUrl = window.location.toString();
//             const indexBeforeId = fullUrl.indexOf("id=");
//             const indexAfterId = fullUrl.indexOf("&action");
//             console.log(`indexBeforeId ${indexBeforeId}, indexAfterId ${indexAfterId}`);
//             var contactId = fullUrl.substring(indexBeforeId + 7, indexAfterId);
//             console.log(`contactId ${contactId}`);
//             return contactId;
//         }
//
//         function submitForm() {
//             $.ajax({
//                 type: "GET",
//                 url: `/mid/create-template`,
//                 success: function (data) {
//                     console.log(typeof data);
//                     console.log('Success! ' + data);
//                     $("body").find(".mid_view").html(data)
//                 },
//                 error: function (data) {
//                     console.log(data);
//                 }
//             });
//         }
//
//         function getAllMidTemplate() {
//             alert("hereqq!");
//             var contactId = 1;
//             $.ajax({
//                 type: "GET",
//                 url: `/get-all-mid/${contactId}`,
//                 success: function (data) {
//                     console.log(typeof data);
//                     console.log('Success! ' + data);
//                     $("body").find(".mid_view_list").html(data)
//                 },
//                 error: function (data) {
//                     console.log(data);
//                 }
//
//             });
//         }
//
//     });
// });
//

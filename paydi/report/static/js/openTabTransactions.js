// Tab top nav
function openTab(evt, tabName) {
                       
    var i, tabcontent, tablinks;

    
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    
    document.getElementById(tabName).style.display = "block";
    var tableName = '#' + tabName + '_table';
    console.log('Table Name = ',tableName);
    evt.currentTarget.className += " active";
    // if (tabName === 'transactions') {
    //     getNewTransactions();
    // } else if (tabName === 'error_transactions') {
    //     getNewErrorTransactions();
    // }
}

//////////////////////////////////////////////
scrollToPagerOf = (ele) => {
    var tabId = ele.nextSibling.nextElementSibling.childNodes[3].id;
    var y = $(window).scrollTop();
    $('html, body').animate({
        scrollTop: y + $(`#${tabId}`).height()
    })
}






//////////////////////////////////////////////
//              FORMATER                    //
//////////////////////////////////////////////

function format ( d ) {
    if (JSON.stringify(d.extract) !== JSON.stringify({})) {
        // `d` is the original data object for the row
        return '<table class="table table-bordered table-responsive-sm text-left w-50" cellpadding="5" cellspacing="5" border="0">'+
            '<tr>'+
                '<td class="col-2">Has Voided:</td>'+
                '<td class="col-5">'+ (d.has_voided ? '<div class="badge badge-success">': '<div class="badge badge-danger">') +d.has_voided+'</div></td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Card number:</td>'+
                '<td class="col-5">'+d.extract.card_number+'</td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Card type:</td>'+
                '<td class="col-5">'+ (d.extract.card_type == 1 ? 'Thẻ quốc tế (không phải MasterCard)' : d.extract.card_type == 2 ? 'Thẻ nội địa' : d.extract.card_type == 3 ? 'Thẻ MasterCard' : 'Loại thẻ không xác định' ) +'</td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Code:</td>'+
                '<td class="col-5"><div class="badge badge-info">'+d.extract.code+'</div></td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Invoice No.:</td>'+
                '<td class="col-5">'+d.extract.invoice_no+'</td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Trace No.:</td>'+
                '<td class="col-5">'+d.extract.trace_no+'</td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Section No.:</td>'+
                '<td class="col-5">'+d.extract.section_no+'</td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Ref No.:</td>'+
                '<td class="col-5">'+d.extract.ref_no+'</td>'+
            '</tr>'+
            '<tr>'+
                '<td class="col-2">Transaction Type:</td>'+
                '<td class="col-5">'+d.extract.tranx_type+'</td>'+
            '</tr>'+
        '</table>';
    } else {
        return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
                '<td>No data.</td>'+
                
            '</tr>'+
        '</table>';
    }
    
}

function error_format ( d ) {
    return '<table class="text-left table table-bordered table-responsive-sm" cellpadding="5" cellspacing="4" border="1" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Card Holder:</td>'+
            '<td>'+d.card_holder+'</td>'+
            '<td>Request Accquired Id:</td>'+
            '<td>'+d.req_acqr_id+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Card number:</td>'+
            '<td>'+d.card_number+'</td>'+
            '<td>Request card type:</td>'+
            '<td>'+d.req_card_type+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Expiration Date:</td>'+
            '<td>'+d.exp_date+'</td>'+
            '<td>Request currency name:</td>'+
            '<td>'+d.req_currency_name+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Tranx Type:</td>'+
            '<td>'+d.tranx_type+'</td>'+
            '<td>Request transactions type:</td>'+
            '<td>'+d.req_tranx_type+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Swipe type:</td>'+
            '<td>'+d.swipe_type+'</td>'+
            '<td>Request transaction amount:</td>'+
            '<td>'+d.req_transaction_amount+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td></td>'+
            '<td></td>'+
            '<td>Request tip amount:</td>'+
            '<td>'+d.req_tip_amount+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td></td>'+
            '<td></td>'+
            '<td>Request merchant transactions Id :</td>'+
            '<td>'+d.req_merchant_trans_id+'</td>'+
        '</tr>'+
    '</table>';
}


function card_format ( d ) {
    return '<table class="text-left table table-bordered table-responsive-sm" cellpadding="5" cellspacing="4" border="1" style="padding-left:50px;">'+
    '<tr>'+
        '<td>Card Holder:</td>'+
        '<td>'+d.card_holder+'</td>'+
        '<td>Request Accquired Id:</td>'+
        '<td>'+d.req_acqr_id+'</td>'+
    '</tr>'+
    '<tr>'+
        '<td>Card number:</td>'+
        '<td>'+d.card_number+'</td>'+
        '<td>Request card type:</td>'+
        '<td>'+d.req_card_type+'</td>'+
    '</tr>'+
    '<tr>'+
        '<td>Expiration Date:</td>'+
        '<td>'+d.exp_date+'</td>'+
        '<td>Request currency name:</td>'+
        '<td>'+d.req_currency_name+'</td>'+
    '</tr>'+
    '<tr>'+
        '<td>Card Type:</td>'+
        '<td>'+d.card_type+'</td>'+
        '<td>Request transactions type:</td>'+
        '<td>'+d.req_tranx_type+'</td>'+
    '</tr>'+
    '<tr>'+
        '<td>Swipe type:</td>'+
        '<td>'+d.swipe_type+'</td>'+
        '<td>Request transaction amount:</td>'+
        '<td>'+d.req_transaction_amount+'</td>'+
    '</tr>'+
    '<tr>'+
        '<td>Currency:</td>'+
        '<td>'+d.currency+'</td>'+
        '<td>Request tip amount:</td>'+
        '<td>'+d.req_tip_amount+'</td>'+
    '</tr>'+
    '<tr>'+
        '<td></td>'+
        '<td></td>'+
        '<td>Request merchant transactions Id :</td>'+
        '<td>'+d.req_merchant_trans_id+'</td>'+
    '</tr>'+
    '<tr>'+
        '<td></td>'+
        '<td></td>'+
        '<td>ISO response code:</td>'+
        '<td class="badge badge-info mt-1 ml-2">'+d.iso_response_code+'</td>'+
    '</tr>'+
'</table>';
}

function pre_auth_format ( d ) {
    if (d.has_voided) {
        return '<table class="text-left table table-bordered table-responsive-sm" cellpadding="5" cellspacing="4" border="1" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Card Holder:</td>'+
            '<td>'+d.void_data.card_holder+'</td>'+
            '<td>Batch No:</td>'+
            '<td>'+d.void_data.batch_no+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Card number:</td>'+
            '<td>'+d.void_data.card_number+'</td>'+
            '<td>Request card type:</td>'+
            '<td>'+d.req_card_type+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Expiration Date:</td>'+
            '<td>'+d.void_data.exp_date+'</td>'+
            '<td>Trace No:</td>'+
            '<td>'+d.void_data.trace_no+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Card Type:</td>'+
            '<td>'+d.void_data.card_type+'</td>'+
            '<td>Request transactions type:</td>'+
            '<td>'+d.void_data.req_tranx_type+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Swipe type:</td>'+
            '<td>'+d.void_data.swipe_type+'</td>'+
            '<td>Request transaction amount:</td>'+
            '<td>'+d.void_data.total_amount+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Currency:</td>'+
            '<td>'+d.void_data.currency+'</td>'+
            '<td>Request time:</td>'+
            '<td>'+d.void_data.trans_date_time+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Code:</td>'+
            '<td>'+d.void_data.code+'</td>'+
            '<td>Request merchant transactions Id :</td>'+
            '<td>'+d.void_data.req_merchant_trans_id+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Description:</td>'+
            '<td>'+d.void_data.desc+'</td>'+
            '<td>ISO response code:</td>'+
            '<td class="badge badge-info mt-1 ml-2">'+d.void_data.iso_response_code+'</td>'+
        '</tr>'+
    '</table>';
    } else {
        return '<table class="text-left table table-bordered table-responsive-sm" cellpadding="5" cellspacing="4" border="1" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Card Holder:</td>'+
            '<td>'+d.card_holder+'</td>'+
            '<td>Batch No:</td>'+
            '<td>'+d.batch_no+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Card number:</td>'+
            '<td>'+d.card_number+'</td>'+
            '<td>Request card type:</td>'+
            '<td>'+d.req_card_type+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Expiration Date:</td>'+
            '<td>'+d.exp_date+'</td>'+
            '<td>Trace No:</td>'+
            '<td>'+d.void_data?.trace_no+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Card Type:</td>'+
            '<td>'+d.card_type+'</td>'+
            '<td>Request transactions type:</td>'+
            '<td>'+d.req_tranx_type+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Swipe type:</td>'+
            '<td>'+d.swipe_type+'</td>'+
            '<td>Request transaction amount:</td>'+
            '<td>'+d.total_amount+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Currency:</td>'+
            '<td>'+d.currency+'</td>'+
            '<td>Request tip amount:</td>'+
            '<td>'+d.req_tip_amount+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Code:</td>'+
            '<td>'+d.code+'</td>'+
            '<td>Request merchant transactions Id :</td>'+
            '<td>'+d.req_merchant_trans_id+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Description:</td>'+
            '<td>'+d.desc+'</td>'+
            '<td>ISO response code:</td>'+
            '<td class="badge badge-info mt-1 ml-2">'+d.iso_response_code+'</td>'+
        '</tr>'+
    '</table>';
    }
}
//////////////////////////////////////////////////////////////////


async function getNewTransactions(){
    const response = await fetch('/report/transactions/data/transactions?offset=0&limit=1');
    const res = await response.json();
    let transactions = res.data;
    $('#loadingLabel1').hide();
    var table = $('#transactions_table').DataTable({
        processing: true,
        serverSide: true,
        info: false,
        bLengthChange: true,
        ajax: {
            url: '/report/transactions/data/transactions',
            type: 'GET',
            dataFilter: function (data) {
                
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.total;
                json.recordsFiltered  = json.total;
                json.data = json.data;
                // console.log(JSON.stringify(json))
                return JSON.stringify(json);
            },
        },
        columns: [
            {
                "className":      'dt-control ',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { data: '_id', title: 'Transaction Id' },
            { data: 'obj_type', title: 'Type' },
            { data: 'status', title: 'Status' },
            { data: 'total_amount', title: 'Total Amount' },
            { data: 'contact', title: 'To Owner Contact Profile',
              render: function( data, type, row, meta ) {
                if(type === 'display' && data !== -1){
                    data = '<a href="/web#id=' + data + '&model=res.partner">Merchant #' + data + '</a>';
                } else if (data === -1) {
                    data = '<p><em class="text-muted">&rarr; Invalid Id &larr;</em></p>'
                }

                return data;
              }
            },
            { data: 'error_msg', title: 'Error Message' },
            { data: 'created_time', title: 'Created Time' },
            
        ],
        columnDefs: [
            {
                targets: [3],
                "render": function ( data, type, row, meta ) {
                    // var table = $('#transactions_table').dataTable().api();
                    if (type === 'display') {
                        var node = table.cell(meta.row, meta.col).nodes().to$();
                        if ( data === 'Success' ) {
                            node.addClass('badge badge-success mt-1');
                        } else if (data = 'Pending'){
                            node.addClass('badge badge-warning mt-1');
                        } else {
                            node.addClass('badge badge-danger mt-1');
                        }
                    }
                    return data;
                }
            },
            {
                targets: [2],
                "render": function ( data, type, row, meta ) {
                    // var table = $('#transactions_table').dataTable().api();
                    if (type === 'display') {
                        var row = table.row(meta.row).nodes().to$();
                        if ( data === 'By Card' ) {
                            row.addClass('bg-light');
                        } else {
                            row.addClass('bg-white');
                        }
                    }
                    return data;
                },
            }
        ],
        "order": [[7, 'desc']]
    });

    table.columns().eq(0).each(function (colIdx) {
        $('input', table.column(colIdx).footer()).on('keyup change', function () {
            table
                .column(colIdx)
                .search(this.value)
                .draw();
        });
    });
    // Add event listener for opening and closing details
    $('#transactions_table tbody').on('click', 'td.dt-control', function () {
        // var table = $('#transactions_table').dataTable().api();
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
         
};


async function getNewErrorTransactions(){
    const response = await fetch('/report/transactions/data/error_transactions?offset=0&limit=1');
    const res = await response.json();
    let transactions = res.data;
    // console.log('Data send to DataTable = ', transactions);
    $('#loadingLabel2').hide();

    // console.log( $('#transactions_table'))
    // asd
    var table = $('#error_transactions_table').DataTable({
        processing: true,
        serverSide: true,
        paging: true,
        info: false,
        ajax: {
            url: '/report/transactions/data/error_transactions',
            type: 'GET',
            dataFilter: function (data) {
                
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.total;
                json.recordsFiltered  = json.total;
                json.data = json.data;
                // console.log(JSON.stringify(json))
                return JSON.stringify(json);
            },
        },
        bLengthChange: true,
        columns: [
            {
                "className":      'dt-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { data: 'pos_id', title: 'Pos Id'},
            { data: 'app_ver', title: 'App Version' },
            { data: 'code', title: 'Code' },
            { data: 'desc', title: 'Description' },
            { data: 'created_time', title: 'Created Time' }
        ],
        "order": [[5, 'desc']]
    });

    // Add event listener for opening and closing details
    $('#error_transactions_table tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( error_format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );     
};


async function getNewCardTransactions(){
    const response = await fetch('/report/transactions/data/card_transactions?offset=0&limit=1');
    const res = await response.json();
    let transactions = res.data;
    // console.log('Data send to DataTable = ', transactions);
    $('#loadingLabel3').hide();

    // console.log( $('#transactions_table'))
    // asd
    var table = $('#card_transactions_table').DataTable({
        processing: true,
        serverSide: true,
        info: false,
        ajax: {
            url: '/report/transactions/data/card_transactions',
            type: 'GET',
            dataFilter: function (data) {
                
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.total;
                json.recordsFiltered  = json.total;
                json.data = json.data;
                // console.log(JSON.stringify(json))
                return JSON.stringify(json);
            },
        },
        bLengthChange: true,
        columns: [
            {
                "className":      'dt-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { data: 'invoice_no', title: 'Invoice No.' },
            { data: 'batch_no', title: 'Batch No.' },
            { data: 'ref_no', title: 'Ref No.' },
            { data: 'trace_no', title: 'Trace No.' },
            { data: 'pos_id', title: 'Pos Id'},
            { data: 'app_ver', title: 'App Version' },
            { data: 'code', title: 'Code' },
            { data: 'total_amount', title: 'Total Amount' },
            { data: 'desc', title: 'Description' },
            { data: 'tranx_type', title: 'Tranx Type' },
            { data: 'trans_date_time', title: 'Tranx Time' },
            { data: 'created_time', title: 'Created Time' }
        ],
        "order": [[12, 'desc']]
    });

    // Add event listener for opening and closing details
    $('#card_transactions_table tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( card_format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );     
};

async function getNewPreAuthTransactions(){
    const response = await fetch('/report/transactions/data/pre_auth_transactions?offset=0&limit=1');
    const res = await response.json();
    let transactions = res.data;
    // console.log('Data send to DataTable = ', transactions);
    $('#loadingLabel4').hide();

    // console.log( $('#transactions_table'))
    // asd
    var table = $('#pre_auth_transactions_table').DataTable({
        processing: true,
        serverSide: true,
        info: false,
        ajax: {
            url: '/report/transactions/data/pre_auth_transactions',
            type: 'GET',
            dataFilter: function (data) {
                
                var json = jQuery.parseJSON(data);
                json.recordsTotal = json.total;
                json.recordsFiltered  = json.total;
                json.data = json.data;
                // console.log(JSON.stringify(json))
                return JSON.stringify(json);
            },
        },
        bLengthChange: true,
        columns: [
            {
                "className":      'dt-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { data: '_id', title: 'Transaction Id' },
            { data: 'invoice_no', title: 'Invoice No.' },
            { data: 'has_voided', title: 'Has Voided' },
            // { data: 'req_card_type', title: 'Request card type' },
            { data: 'section_no', title: 'Section No.' },
            
        ],
        columnDefs: [
            {
                targets: [3],
                "render": function ( data, type, row, meta ) {
                    // var table = $('#pre_auth_transactions_table').dataTable().api();
                    if (type === 'display') {
                        var node = table.cell(meta.row, meta.col).nodes().to$();
                        if ( data === true ) {
                            node.addClass('badge badge-success mt-1 ml-2');
                        } else {
                            node.addClass('badge badge-danger mt-1 ml-2');
                        }
                    }
                    return data;
                }
            },
        ],
        "order": [[1, 'desc']]
    });

    // Add event listener for opening and closing details
    $('#pre_auth_transactions_table tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( pre_auth_format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );     
};
//////////////////////////////////////////////////////////////////
$( document ).ready(function() {
    console.log( "ready!" );
    document.getElementById("defaultOpen").click();
    getNewTransactions();
    getNewErrorTransactions();
    getNewCardTransactions();
    getNewPreAuthTransactions();

    // mybutton = document.getElementById("myBtn");
    // function topFunction() {
    //     var y = $(window).scrollTop();
    //     $('html, body').animate({
    //         scrollTop: y
    //     });
    // }

});






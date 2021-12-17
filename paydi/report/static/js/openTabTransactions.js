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
}

//////////////////////////////////////////////

scrollToPager = () => {
    var y = $(window).scrollTop();
    $('html, body').animate({
        scrollTop: y + $('#transactions_table').height()
    })
}

/////////////////////////////////////////////



function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Batch No.:</td>'+
            '<td>'+d.extract.batch_no+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Card number:</td>'+
            '<td>'+d.extract.card_number+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Card type:</td>'+
            '<td>'+d.extract.card_type+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Code:</td>'+
            '<td>'+d.extract.code+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Swipe type:</td>'+
            '<td>'+d.extract.swipe_type+'</td>'+
        '</tr>'+
    '</table>';
}



async function getNewTransactions(){
    document.getElementById("defaultOpen").click();
    const response = await fetch('/report/transactions/data/transactions/');
    const res = await response.json();
    let transactions = res.data;
    console.log('Data send to DataTable = ', transactions);
    $('#loadingLabel1').hide();

    // console.log( $('#transactions_table'))
    // asd
    var table = $('#transactions_table').DataTable({
        data: transactions,
        bLengthChange: true,
        columns: [
            {
                "className":      'dt-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { data: 'obj_type', title: 'Type' },
            { data: 'status', title: 'Status' },
            { data: 'total_amount', title: 'Total Amount' },
            { data: 'error_msg', title: 'Error Message' },
            { data: 'created_time', title: 'Created Time' }
        ],
        columnDefs: [
            {
                targets: [2],
                "render": function ( data, type, row, meta ) {
                    var table = $('#transactions_table').dataTable().api();
                    if (type === 'display') {
                        var node = table.cell(meta.row, meta.col).nodes().to$();
                        if ( data === 'Success' ) {
                            node.addClass('badge badge-success mt-1');
                        } else {
                            node.addClass('badge badge-danger mt-1');
                        }
                    }
                    return data;
                }
            },
            {
                targets: [1],
                "render": function ( data, type, row, meta ) {
                    var table = $('#transactions_table').dataTable().api();
                    if (type === 'display') {
                        var row = table.row(meta.row).nodes().to$();
                        if ( data === 'By Card' ) {
                            row.addClass('bg-light');
                        } else {
                            row.addClass('bg-white');
                        }
                    }
                    return data;
                }
            }
        ],
        "order": [[5, 'desc']]
    });

    // Add event listener for opening and closing details
    $('#transactions_table tbody').on('click', 'td.dt-control', function () {
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

var table = getNewTransactions();



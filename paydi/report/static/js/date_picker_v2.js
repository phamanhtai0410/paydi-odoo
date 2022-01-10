$( function() {
    var dateFormat = "dd/mm/yy",
    from = $( "#from" ).datepicker({
        dateFormat: 'dd/mm/yy',
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 3
    })
    .on( "change", function() {
        to.datepicker( "option", "minDate", getDate( this ) );
    }),
    to = $( "#to" ).datepicker({
        dateFormat: 'dd/mm/yy',
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 3
    })
    .on( "change", function() {
        from.datepicker( "option", "maxDate", getDate( this ) );
    });

    function getDate( element ) {
        var date;
        try {
            console.log('element = ', element.value)
            date = $.datepicker.parseDate( dateFormat, element.value );
            console.log('Date picker parse date = ', date)
        } catch( error ) {
            date = null;
        }

        return date;
    }
} );
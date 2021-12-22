scrollToPager = () => {
    var y = $(window).scrollTop();
    $('html, body').animate({
        scrollTop: y + $('#transactions_table').height()
    })
}

scrollToErrorPager = () => {
    var y = $(window).scrollTop();
    $('html, body').animate({
        scrollTop: y + $('#transactions_table').height()
    })
}
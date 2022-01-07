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
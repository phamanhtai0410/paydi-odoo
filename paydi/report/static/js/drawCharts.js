var chartByMethodTotalAmount,
    chartByMethodTotalTransactions,
    chartByCardTypeTotalAmount,
    chartByCardTypeTotalTransactions;

async function draw_charts(from_date='', to_date='') {
    const response = await fetch(`/report/transactions/statistics?from=${from_date}&to=${to_date}`);
    const res = await response.json();
    console.log('Fetch data : ', res);


    // var xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
    // var yValues = [55, 49, 44, 24, 15];
    // var barColors = [
    //     "#b91d47",
    //     "#00aba9",
    //     "#2b5797",
    //     "#e8c3b9",
    //     "#1e7145"
    // ];


    // Data
    var xValuesByMethod = ["By Card", "By QR Code"];
    var yValuesByMethodTotalAmount = [
        res.card.total_amount,
        res.qr_code.total_amount
    ];
    var yValuesByMethodTotalTransactions = [
        res.card.total_transactions,
        res.qr_code.total_transactions
    ];
    var barColorsByMethod = [
        "#2b5797",
        "#00aba9"
    ];

    var xValuesByCardType = [
        res.card.types[0].name,
        res.card.types[1].name,
        res.card.types[2].name
    ];
    var yValuesByCardTypeTotalAmount = [
        res.card.types[0].total_amount,
        res.card.types[1].total_amount,
        res.card.types[2].total_amount
    ];
    var yValuesByCardTypeTotalTransactions = [
        res.card.types[0].total_transactions,
        res.card.types[1].total_transactions,
        res.card.types[2].total_transactions
    ];
    var barColorsByCardType = [
        "#b91d47",
        "#2b5797",
        "#00aba9"
    ];


    // <!-- Draw Charts -->
    if (chartByMethodTotalAmount != null) {
        chartByMethodTotalAmount.destroy();
    }
    chartByMethodTotalAmount = new Chart("byMethodTotalAmountChart", {
        type: "doughnut",
        data: {
            labels: xValuesByMethod,
            datasets: [{
                backgroundColor: barColorsByMethod,
                data: yValuesByMethodTotalAmount
            }]
        },
        options: {
            layout: {
                padding: 20
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'TOTAL AMOUNT By Payment Method'
                }
            }
        }
    });
    document.getElementById("byMethodTotalAmountChart").style.display = '';
    
    if (chartByCardTypeTotalAmount != null) {
        chartByCardTypeTotalAmount.destroy();
    }
    chartByCardTypeTotalAmount = new Chart("byCardTypeTotalAmountChart", {
        type: "doughnut",
        data: {
            labels: xValuesByCardType,
            datasets: [{
                backgroundColor: barColorsByCardType,
                data: yValuesByCardTypeTotalAmount
            }]
        },
        options: {
            layout: {
                padding: 20
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'TOTAL AMOUNT By Card Type'
                }
            }
        }
    });
    document.getElementById("byCardTypeTotalAmountChart").style.display = '';

    if (chartByMethodTotalTransactions != null) {
        chartByMethodTotalTransactions.destroy();
    }
    chartByMethodTotalTransactions = new Chart("byMethodTotalTransactionsChart", {
        type: "doughnut",
        data: {
            labels: xValuesByMethod,
            datasets: [{
                backgroundColor: barColorsByMethod,
                data: yValuesByMethodTotalTransactions
            }]
        },
        options: {
            layout: {
                padding: 20
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'TOTAL TRANSACTIONS by Payment Method'
                }
            }
        }
    });
    document.getElementById("byMethodTotalTransactionsChart").style.display = '';

    if (chartByCardTypeTotalTransactions != null) {
        chartByCardTypeTotalTransactions.destroy();
    }
    chartByCardTypeTotalTransactions = new Chart("byCardTypeTotalTransactionsChart", {
        type: "doughnut",
        data: {
            labels: xValuesByCardType,
            datasets: [{
                backgroundColor: barColorsByCardType,
                data: yValuesByCardTypeTotalTransactions
            }]
        },
        options: {
            layout: {
                padding: 20
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'TOTAL TRANSACTIONS By Card Type'
                }
            }
        }
    });
    document.getElementById("byCardTypeTotalTransactionsChart").style.display = '';
};


document.getElementById("defaultOpen").click();

async function getCharts() {
    $('#loading').css('display', 'block');
    await draw_charts();
    $('#loading').hide();
}
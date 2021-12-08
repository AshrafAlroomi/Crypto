// elements ids
const PROFIT_ID = ""
const TRADE_TABLE = "trade_list"
const TRADE_LIST = "trade_list_body"
const HOLD_LIST = "hold_list_body"

const update_trades = (data) => {
    /*
     <th>Order</th>
     <th>#</th>
     <th>Coin</th>
     <th>price</th>
     <th>profit</th>
     */
    if (!data) {
        return 0;
    }

    var table = document.getElementById(TRADE_LIST);
    table.innerHTML = ""
    for (let i = 0; i < data.length; i++) {
        var row = table.insertRow(0);
        //row.style.backgroundColor = "#03233a"

        var c0 = row.insertCell(0);
        c0.innerHTML = data[i].order;

        var c1 = row.insertCell(1);
        c1.innerHTML = data[i].quantity;

        var c2 = row.insertCell(2);
        c2.innerHTML = data[i].name;

        var c3 = row.insertCell(3);
        c3.innerHTML = data[i].price;

        var c4 = row.insertCell(4);
        c4.innerHTML = data[i].profit;
        if (data[i].profit > 0.0) {
            c4.style.backgroundColor = "#64f839"
        } else if (data[i].profit < 0.0) {
            c4.style.backgroundColor = "#ec2323"
        } else {

        }

    }

}
const update_holds = (data) => {
    /*
    <th>symbol</th>
    <th>#</th>
    <th>price</th>
    <th>cost</th>
     */
    if (!data) {
        return 0;
    }
    var table = document.getElementById(HOLD_LIST);
    table.innerHTML = "";

    for (let i = 0; i < data.length; i++) {
        var row = table.insertRow(0);

        var c0 = row.insertCell(0);
        c0.innerHTML = data[i].symbol;

        var c1 = row.insertCell(1);
        c1.innerHTML = data[i].quantity;

        var c2 = row.insertCell(2);
        c2.innerHTML = data[i].price;

        var c3 = row.insertCell(3);
        c3.innerHTML = data[i].cost;
    }

}
const update_cards = (data) => {
    if (!data || !Object.keys(data).length) {
        return 0;
    }
    document.getElementById("profit").innerHTML = data.profit.toFixed(2)
    document.getElementById("balance").innerHTML = data.balance.toFixed(2)
    document.getElementById("assets").innerHTML = data.assets.toFixed(2)
    document.getElementById("period").innerHTML = data.period


}

const update_button = () => {

}
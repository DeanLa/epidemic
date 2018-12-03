var p = parseInt(pick.active);
if (p === 1) {
    $("#main-chart-total").hide();
    $("#main-chart-split").show();
} else if (p === 0) {
    $("#main-chart-total").show();
    $("#main-chart-split").hide();
}
var d = ds.value;
var heb = translate[d];
var s = ss.value;
var p = pick.active;
var mind = Math.floor(parseInt(xr.start.toString()) / 1000);
var maxd = Math.floor(parseInt(xr.end.toString()) / 1000);
history.pushState({},
    'Epidemic  - ' + d,
    '/dashboard?' +
    'disease=' + d +
    '&smooth=' + s +
    '&split=' + p +
    '&min_date=' + mind +
    '&max_date=' + maxd
);

base_title = 'כמות מקרים שנתית - ';
$(".disease").html(heb);

var l1 = "https://www.facebook.com/sharer/sharer.php?u=";
var l2 = "%2F&amp;src=sdkpreparse";

$("#u_0_1").attr("href",l1 + window.location.search + l2);
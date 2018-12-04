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
console.log(translate);
console.log(d);

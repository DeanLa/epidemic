var d = ds.value;
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
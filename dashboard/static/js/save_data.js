var cols = ['date', 'total', 'afula', 'akko', 'ashqelon', 'beer_sheva', 'hasharon', 'hadera', 'haifa', 'jerusalem', 'kinneret',
    'nazareth', 'petach_tiqwa', 'ramla', 'rehovot', 'tel_aviv', 'zefat'];
var data = source.data;
console.log(data);
var filetext = cols.join().concat('\n');
for (var i = 0; i < data['date'].length; i++) {
    var dt = new Date(data['date'][i]);
    var dts = dt.getFullYear().toString() + '-' +
        ("0" + (dt.getMonth() + 1)).slice(-2) + '-' +
        ("0" + dt.getDate()).slice(-2);
    var currRow = cols.map(col => data[col][i].toString());
    currRow[0] = dts;
    var joined = currRow.join().concat('\n');
    filetext = filetext.concat(joined);
}
filetext = filetext.replace("NaN","");
var filename = save_path;
var blob = new Blob([filetext], {type: 'text/csv;charset=utf-8;'});
//
//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
} else {
    var link;
    link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}
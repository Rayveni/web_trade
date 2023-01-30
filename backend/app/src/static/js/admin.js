var  hot2;

function process_htable(obj, dropdown_id) {
    let _checked=document.getElementById("auto_csv").checked,
        selected_table=obj.text,
        query_string='/query_data?table=';
    query_string=query_string.concat(selected_table);




    if(_checked){dropdown_show(dropdown_id);
query_string=query_string.concat('&csv=1');

let  x=new XMLHttpRequest();
x.open( "GET", query_string , true);
x.responseType="blob";
x.onload= function(e){download(e.target.response, selected_table+".csv", "text/csv");};
x.send();


  ; return 1}

    let table_data = get_data_to_js(query_string);
    var settings1 = {
        data: table_data.slice(1),
        colHeaders: table_data[0],
        manualColumnResize: true,
        autoWrapRow: true,
        // manualRowResize: true,
        //manualRowMove: true,
        manualColumnMove: true,
        // stretchH: "all",
        licenseKey: 'non-commercial-and-evaluation'
    }

    document.getElementById('button_drp_id_1').innerHTML = obj.text;
    var handsome_container = document.getElementById('h_table_id');

    handsome_container.innerHTML = ""
        hot2 = new Handsontable(handsome_container, settings1);
    dropdown_show(dropdown_id);

}

function drop_db_table(obj, dropdown_id) {
if (confirm("drop "+obj.text +"?")) {

$.post( "/upload_mongo_form", {
   'submit_button':'drop_table','table':obj.text
}); 
} ;


dropdown_show(dropdown_id);


}

function function_export_csv_() {
	    hot2.getPlugin("exportFile").downloadFile("csv", {
        filename: "table export",
        columnDelimiter: ';',
        columnHeaders: true

    });
};
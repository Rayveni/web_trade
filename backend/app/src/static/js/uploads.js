
var data_arr = get_data_to_js('/api/query_data?table=upload_mosex_sec'),
   handsome_container = document.getElementById('h_table_id'),
   hot2;







function process_htable(table_data) {
    var settings1 = {
        data: table_data.slice(1),
        colHeaders: data_arr[0],
        manualColumnResize: true,
        autoWrapRow: true, //,contextMenu: true,rowHeaders: true,maxRows: 2000,

        //rowHeaders: true,
        readOnly: true,
   
        // hiddenColumns: {
        // columns: exclude_columns(table_data.columns,exclude_list),
        //  },
        // manualRowResize: true,
        //manualRowMove: true,
        manualColumnMove: true,
        // stretchH: "all",
        licenseKey: 'non-commercial-and-evaluation'
    }

    handsome_container.innerHTML = ""
        hot2 = new Handsontable(handsome_container, settings1);
};



function function_export_csv_() {
	    hot2.getPlugin("exportFile").downloadFile("csv", {
        filename: "table export",
        columnDelimiter: ';',
        columnHeaders: true

    });
};

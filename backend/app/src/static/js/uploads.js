
var data_arr = get_data_to_js('/api/query_data?table=upload_mosex_sec'),
   handsome_container = document.getElementById('h_table_id'),
   hot2,
   tasks_in_queue=document.getElementById('tasks_in_queue') ,
   failed_uploads=document.getElementById('failed_uploads')
   ;
const success_ind=data_arr[0].indexOf("success");   
function firstRowRenderer(instance, td, row, col, prop, value, cellProperties) {
	Handsontable.renderers.TextRenderer.apply(this, arguments);
  if (value== true){
  td.style.background = '#d4edda';
  }else {
	  td.style.background = '#f8d7da';
  }
}
function process_htable(table_data) {
    var settings1 = {
        data: table_data.slice(1),
        colHeaders: data_arr[0],
        manualColumnResize: true,
        autoWrapRow: true, //,contextMenu: true,rowHeaders: true,maxRows: 2000,
        multiColumnSorting: {
            indicator: true,
            sortEmptyCells: true,
            //initialConfig: {
            //    column: new_cols.indexOf("pers_profit"),
            //   sortOrder: 'desc'
            //}
        },
        //rowHeaders: true,
        readOnly: true,
   
        // hiddenColumns: {
        // columns: exclude_columns(table_data.columns,exclude_list),
        //  },
        // manualRowResize: true,
        //manualRowMove: true,
        manualColumnMove: true,
        // stretchH: "all",
        licenseKey: 'non-commercial-and-evaluation',
		  cells: function (row, col) {
    var cellProperties = {};



    if (col === success_ind) {
      cellProperties.renderer = firstRowRenderer; // uses function directly
    }


    return cellProperties;
  }
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
process_htable(data_arr);

function calc_success_tasks() {
		let counter=0;
       data_arr.forEach(function(elem) {
	 if (elem[success_ind] == true) {
            counter++;
        }
});

 return counter;
};


const sheduleed_tasks=get_data_to_js('/api/queue_info?report=count');
tasks_in_queue.textContent="Sheduled tasks: "+sheduleed_tasks.toString();


let failed_uploads_value=data_arr.length-1-calc_success_tasks();
failed_uploads.textContent="Failed to update securities:"+failed_uploads_value.toString();



  if (sheduleed_tasks > 0) {
    tasks_in_queue.classList.add('highlight_danger');
  } else {
    tasks_in_queue.classList.add('highlight_success');
  }
  
    if (failed_uploads_value > 0) {
    failed_uploads.classList.add('highlight_danger');
  } else {
    failed_uploads.classList.add('highlight_success');
  }
  
  

function generate_table_from_array(table, data, header_first_row = 1) {
    let slice_start = 0;
    if (header_first_row == 1) {
        let thead = table.createTHead();
        let row = thead.insertRow();
        for (let key of data[0]) {
            let th = document.createElement("th");
            let text = document.createTextNode(key);
            th.appendChild(text);
            row.appendChild(th);
        }
        slice_start = 1;
    }
    let tbody=table.createTBody();
    for (let element of data.slice(slice_start)) {
        let row = tbody.insertRow();
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
    }

}

function merge_table_rows(table, column) {
    let rows_count = table.rows.length;
    var i,
    row_id1 = 1,
    row_val1 = table.rows[1].cells[column].innerHTML;
    var temp_val,
    temp_id,
    row_span_count = 1;
    for (i = 2; i < rows_count; i++) {
        temp_val = table.rows[i].cells[column].innerHTML;
        if ((temp_val == row_val1)) {
            row_span_count = row_span_count + 1;
            table.rows[i].deleteCell(column);
        } else {
            if (row_span_count > 1) {
                table.rows[row_id1].cells[column].rowSpan = row_span_count;
            }
            row_span_count = 1;
            row_val1 = temp_val;
            row_id1 = i;

        }
    }
    if (row_span_count > 1) {
        table.rows[row_id1].cells[column].rowSpan = row_span_count;
    }

    //table.rows[1].cells[0].rowSpan=3
    //table.rows[2].deleteCell(0)

}
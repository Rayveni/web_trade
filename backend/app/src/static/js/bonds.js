var default_start = today(3),
default_end = today(6),
max_profit_value = 30,
current_tab="",
hot2;

document.getElementById("max_profit_id").value = max_profit_value;

function draw_daterangepicker(element_id, default_date, start_date = true) {
	
        $('#'+element_id).daterangepicker({
        "singleDatePicker": true,
        "showWeekNumbers": true,
        "autoApply": true,
        "locale": {
            "format": "YYYY-MM-DD"
        },
        "startDate": default_date,

    }, function (start, end, label) {
	
        if (start_date) {
            default_start = end.format('YYYY-MM-DD');
        } else {
            default_end = end.format('YYYY-MM-DD');
        }
        if (current_tab != "")
            draw_hs_table("", current_tab);
    });
};

draw_daterangepicker('start_date',default_start);
draw_daterangepicker('end_date',default_end,false);

function increaseEndDate() {
    const new_date = today(3, default_end);
    draw_daterangepicker('end_date', new_date, false);

    default_end = new_date;

    if (current_tab != "")
        draw_hs_table("", current_tab);
};
function ofertaCheckboxEvent(){
	if (current_tab!="" )draw_hs_table("",current_tab);
}
function handleInputChange(val) {
    max_profit_value = parseInt(val);
	if (current_tab!="" )draw_hs_table("",current_tab);
};

function crossfilter_coverter(table_name) {
    data_arr = get_data_to_js('/query_data?table=' + table_name)
        const red_index = data_arr[0].indexOf('redemption'),
		     sec_name_index=data_arr[0].indexOf('sec_name'),
		     ticker_index=data_arr[0].indexOf('ticker');
        return {
        columns: data_arr[0],
        data: crossfilter(data_arr.slice(1).map(function (row) {
                row[red_index] = row[red_index].substring(0, 10);
				 row[sec_name_index] = "<a href='https://smart-lab.ru/q/bonds/" +row[ticker_index]+"/' target='_blank'>" +row[sec_name_index]+"</a>"
				
                return row
            })),
    };
};

var rubonds = crossfilter_coverter('smartlabbondsrus');

var eurbonds = crossfilter_coverter('smartlabbondsusd');
var handsome_container = document.getElementById('h_table_id');
var checkbox_crl = document.getElementById('oferta_checkbox');

function bonds_filter(bonds_cf, bond_category) {
    const bond_cat_index = bonds_cf.columns.indexOf("bond_category"),
    pers_profit_index = bonds_cf.columns.indexOf("pers_profit"),
    redemption_index = bonds_cf.columns.indexOf("redemption"),
    default_start_mom = moment(default_start),
    default_end_mom = moment(default_end);

    var topicsDim = bonds_cf.data.dimension(function (d) {
            return {
                bond_cat: d[bond_cat_index],
                pers_profit: d[pers_profit_index],
                redempt: moment(d[redemption_index])
            };
        });
    if (isNaN(max_profit_value)) {
        topicsDim.filter(function (d) {
            return d.bond_cat == bond_category && d.redempt >= default_start_mom && d.redempt <= default_end_mom
        })
    } else {
        topicsDim.filter(function (d) {
            return d.bond_cat == bond_category && d.pers_profit <= max_profit_value && d.redempt >= default_start_mom && d.redempt <= default_end_mom
        })
    }
    var filtered_data = topicsDim.top(Infinity);
    topicsDim.filterAll();
    return {
        columns: bonds_cf.columns,
        data: filtered_data,
    };
};

function add_data_type(el) {
    const d_dict = {
        "redemption": ",type: 'date',correctFormat: false,dateFormat: 'YYYY-MM-DD'",
		"sec_name":', renderer: "html"'
    }
    add_item = d_dict[el];
    if (add_item == undefined) {
        res = "";
    } else {
        res = add_item;
    }
    return res;
};
function exclude_columns(data_columns, exclude_list) {
    if (checkbox_crl.checked) {
        exclude_list.push('oferta')
    }
    var excluded_cols = exclude_list.map(_column => data_columns.indexOf(_column));
    left_col = [...Array(data_columns.length).keys()].filter(x => !excluded_cols.includes(x));

    return [left_col, "[" + left_col.map(_column => '{data: ' + _column + add_data_type(data_columns[_column]) + '}').join(',') + "]"];
};

function rename_columns(columns) {
    res = []
    const r_dict = {

        "sec_name": "Имя<br>&#8203; ",
        "redemption": "Погашение<br>&#8203;",
        "oferta": "Оферта<br>&#8203;",
        "years_till_redemption": "Лет до<br/>погаш.",
        "annual_bond_pers_profit": "Куп.дох.<br>отн.номинала",
        //"duraction_years",
        "ofz_type": "Тип<br>ОФЗ",
        "pers_profit": "Доходн<br>&#8203;",
        "last_deals_bond_pers_profit": "Куп.Дох.<br/> посл. сделки",
        "price": "Цена<br>&#8203;",
        //"volume_rur_mln",
        //"bond_rur",
        // "bond_date"
    }
    columns.forEach(function (item) {
        add_item = r_dict[item]
            if (add_item == undefined) {
                res.push(item + '<br>&#8203;');
            } else {
                res.push(add_item);
            }

    });
    return res;
};

function process_htable(table_data, exclude_list) {
    const _columns = exclude_columns(table_data.columns, exclude_list),
    new_cols = _columns[0].map(_column => table_data.columns[_column]);

    var settings1 = {
        data: table_data.data,
        colHeaders: rename_columns(new_cols),
        manualColumnResize: true,
        autoWrapRow: true, //,contextMenu: true,rowHeaders: true,maxRows: 2000,

        //rowHeaders: true,
        readOnly: true,

        multiColumnSorting: {
            indicator: true,
            sortEmptyCells: true,
            initialConfig: {
                column: new_cols.indexOf("pers_profit"),
                sortOrder: 'desc'
            }
        },
        columns: eval(_columns[1]),
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

function draw_hs_table(evt,bond_category) {

    if (bond_category == 'ЕВРО') {
        const exclude_list = ['bond_category',
            "last_deal",
            "sys_updated",
            "years_till_redemption",
            "volume_thousand_usd",
            "nkd_usd",
            "bond_date",
            "frequency_in_year"];
        process_htable(
		bonds_filter(eurbonds, "Еврооблигации")
		/*{
            columns: eurbonds.columns,
            data:  eurbonds.data.all()
        }*/, exclude_list);
    } else {
        var exclude_list = ['bond_category',
            "last_deal",
            "sys_updated",
            "years_till_redemption",
            "volume_rur_mln",
            "nkd_rur",
            "bond_date",
            "frequency_in_year"];
        if (bond_category != 'ОФЗ') {
            exclude_list.push('ofz_type')
        }
        process_htable(bonds_filter(rubonds, bond_category), exclude_list);
    }
	if (current_tab != bond_category) {
	    tablinks = document.getElementsByClassName("tablinks");
	    for (i = 0; i < tablinks.length; i++) {
	        tablinks[i].className = tablinks[i].className.replace(" active", "");
	    }
	    evt.currentTarget.className += " active";
	    current_tab = bond_category;
	}
};

function function_export_csv_() {
	    hot2.getPlugin("exportFile").downloadFile("csv", {
        filename: "table export",
        columnDelimiter: ';',
        columnHeaders: true

    });
};

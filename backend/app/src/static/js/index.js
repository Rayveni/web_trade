var url_base='/query_data?view_id=open_broker_report&params=',
	handsome_container = document.getElementById('h_table_id'),
	assets_data,
	report_state=["Assets",0];
	sectors_data=[],
	tab_panel1=document.getElementById("tab_1"),
	tab_panel2=document.getElementById("tab_2");

const agreement_ids = ['_173364_','_173364i_'],
	  gradient_colour1='#33CCCC',
	  gradient_colour2="white";

function main() {
    set_total_account_html(prepare_data_account_total());
	get_assets();
	process_htable(assets_data[0], gradient_cols = [2]);
	create_tabs();
	agg_assets();
	set_active_panel(tab_panel2,"total");
	set_active_panel(tab_panel1,"Assets");
}
function set_active_panel(panel,value){
	let tablinks = panel.getElementsByClassName("tablinks");
	    tablinks.forEach((tablink) => {
        tablink.className =tablink.className.replace(" active", "");
		if (tablink.textContent==value){
			tablink.className += " active";
			
		}
		
        })
}

function agg_assets() {
    sectors_data.push(calc_sector_industry_view("industry", 4));
    sectors_data.push(calc_sector_industry_view("sector", 5));

}
function calc_sector_industry_view(grouper_name, col_id) {

    return assets_data.map(function (_dataset) {
        let header = [[grouper_name, "amount"]],
        temp;
        temp = groupby_sum(_dataset.slice(1), col_id, 2);
        for ([_key, _val]of Object.entries(temp)) {
            header.push([_key, _val])
        }
        return header
    });

}

function get_assets() {
    let _arr = [],
    total = {},
    sec_sectors,
    total_sum = 0,
    s,
    row,
    temp_data,
    _filter = ["asset_name",
        "settlement_fact_cb",
        "position_weight_cb"
    ],
    template_arr = [["ticker", "asset_name", "amount", "amount,%", "industry", "sector", "action"]],
    temp_arr = [];
    for (let i = 0; i < agreement_ids.length; i++) {
        temp_data = get_data_to_js(url_base + agreement_ids[i])["assets"];
        temp_arr = Object.assign([], template_arr)
            for ([_key, _val]of Object.entries(temp_data)) {
                s = _val["asset_name"];
                if (s == undefined) {
                    s = ""
                };
                s = s.trim();
                temp_arr.push([_key,
                        s,
                        parseFloat((_val["settlement_fact_cb"] * 1).toFixed(2)),
                        parseFloat((_val["position_weight_cb"] * 1).toFixed(1)),
                        "",
                        "",
                        ""
                    ]);

                if (total.hasOwnProperty(_key)) {
                    row = total[_key];
                    row[1] = row[1] + parseFloat(_val["settlement_fact_cb"]);
                    total[_key] = row;
                } else {
                    total[_key] = [s, parseFloat(_val["settlement_fact_cb"])];
                }
                total_sum = total_sum + parseFloat(_val["settlement_fact_cb"]);
            }
            _arr.push(temp_arr)
    }

    temp_data = prepare_total(total, total_sum, template_arr);

    sec_sectors = get_sec_sectors(temp_data[1]);
    temp_data = [temp_data[0]].concat(_arr);
    assets_data=add_info_assets(temp_data, sec_sectors);
    //return add_info_assets(temp_data, sec_sectors);
}

function add_info_assets(assets_arr, sectors_dict) {
    let asset,
    key;
    for (let i = 0; i < assets_arr.length; i++) {
        asset = assets_arr[i];

        for (let j = 1; j < asset.length; j++) {

            key = find_sec_with_pref(asset[j][0], sectors_dict);

            if (key === undefined) {}
            else {
                asset[j][4] = key['industry'];
                asset[j][5] = key['sector'];
                asset[j][6] = key['action'];
            }
        }
    }
    return assets_arr;
}

function find_sec_with_pref(_sec, _dict) {
    let res;
    res = _dict[_sec];
    if (res === undefined) {
        if (_sec.slice(-1) == 'P') {
            res = _dict[_sec.slice(0, -1)];
        }
    }
    return res;
}

function prepare_total(total_dict, total_sum, template_arr) {
    let _arr = [];
    for ([_key, _val]of Object.entries(total_dict)) {
        template_arr.push([_key,
                _val[0],
                parseFloat((_val[1] * 1).toFixed(2)),
                parseFloat((100 * _val[1] / total_sum).toFixed(1)),
                "",
                "",
                ""
            ])
        _arr.push(_key);
        if (_key.slice(-1) == 'P') {
            _arr.push(_key.slice(0, -1))
        }
    }
    return [template_arr, _arr];
}
function get_sec_sectors(arr) {
    let url = "/query_data?table=sec_sector&noconvert=1",
    _post = {
        'query': {
            'ticker': {
                '$in': arr
            }
        },
        'dict_key': "ticker",
        'result': 'dict',
        'columns': ['action', 'industry', 'sector', 'ticker']
    };
    return get_data_to_js(url, _post)

}
function prepare_data_account_total() {
    let table_data,
    raw_data_arr = [["start date", "end date", "Market Value", "Invested"]],
    temp_data,
    temp_data2,
    sum_assets = 0,
    sum_non_trade_currency = 0,
    slice1,
    slice2;
    for (let i = 0; i < agreement_ids.length; i++) {
        temp_data = get_data_to_js(url_base+agreement_ids[i]);
        raw_data_arr.push([temp_data["period"][0],
                temp_data["period"][1],
                temp_data["assets_cb_value"]["RUB"]["value"],
                temp_data["non_trade_currency"]["RUB"]
            ]);
        sum_assets = sum_assets + temp_data["assets_cb_value"]["RUB"]["value"];
        sum_non_trade_currency = sum_non_trade_currency + temp_data["non_trade_currency"]["RUB"];
    }
    raw_data_arr.push(["", "", sum_assets, sum_non_trade_currency]);
    raw_data_arr = raw_data_arr[0].map((_, colIndex) => raw_data_arr.map(row => row[colIndex]));

    slice1 = raw_data_arr[2];
    slice2 = raw_data_arr[3];

    let pl = ["P&L"],
    pl_pers = ["P&L%"];
    for (let i = 1; i < raw_data_arr[0].length; i++) {
        temp_data = slice1[i];
        temp_data2 = slice2[i];
        pl.push(temp_data - temp_data2);
        pl_pers.push((temp_data - temp_data2) / temp_data);
    }
    raw_data_arr.push(pl);
    raw_data_arr.push(pl_pers);
    raw_data_arr.unshift(["","173364","173364i","Total"])

    return raw_data_arr;
}

function set_total_account_html(_data) {
    let _header=document.getElementById("holdings_header");
	//_header.textContent=_header.textContent.replace("start",period[0]).replace("end",period[1]);
    let card_holdings_overview = document.getElementById('acc_total'),
    tbl = document.createElement("table");
    tbl.id = "acc_total_table_id";

	for (let i = 1; i < _data[0].length; i++) {
		for (let j = 3; j < 6; j++) {
			_data[j][i] = currency_print(_data[j][i], "RUB", locale = 'ru');
		}
		_data[6][i] = parseFloat(100*_data[6][i]).toFixed(2) + "%";
	};
    generate_table_from_array(tbl, _data);
    card_holdings_overview.appendChild(tbl);
}

function calc_max_from_matrix(matrix, column, start_row = 1) {
    let max_val = matrix[start_row][column],
    temp_val;
    for (let i = start_row + 1; i < matrix.length; i++) {
        temp_val = matrix[i][column];
        if (max_val < temp_val) {
            max_val = temp_val;
        }
    }
    return max_val;
}

function process_htable(table_data, gradient_cols) {
    //calc_max_from_matrix(table_data,2);
    let gradient_dict = {};
    gradient_cols.forEach((element) => {
        gradient_dict[element] = calc_max_from_matrix(table_data, element);
    });

    var settings1 = {
        data: table_data.slice(1),
        colHeaders: table_data[0],
        manualColumnResize: true,
        autoWrapRow: true, //,contextMenu: true,rowHeaders: true,maxRows: 2000,
        //rowHeaders: true,
        readOnly: true,

        multiColumnSorting: {
            indicator: true,
            sortEmptyCells: true,
            initialConfig: {
               column: 1,
                sortOrder: 'asc'
            }
        },
        // columns: eval(_columns[1]),
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
            cellProperties.gradient = gradient_dict;
            cellProperties.renderer = conditionalFormatRenderer;

            return cellProperties;
        }
    }
    handsome_container.innerHTML = ""
        hot2 = new Handsontable(handsome_container, settings1);
};

  function conditionalFormatRenderer(instance, td, row, col, prop, value, cellProperties) {
      Handsontable.renderers.TextRenderer.apply(this, arguments);
      let percent,
      max_val,
      gradient_d = cellProperties.gradient;

      if (parseInt(value, 10) < 0) {
          td.style.color = 'red'
      } else {
          try {
              max_val = gradient_d[col];
              percent = Math.round(value / max_val * 100);
              // td.style.background = "linear-gradient(90deg, "+gradient_colour+",white " + percent + "%)";
              td.style.background = "-webkit-gradient(linear, left top,right top, color-stop(" + percent + "%," + gradient_colour1 + "), color-stop(" + percent + "%," + gradient_colour2 + "))";
          } catch {};
      }
  };

function create_tabs() {
    let tab_parent = document.getElementById("tab_2"),
    _agreements = ['total'].concat(Object.assign([], agreement_ids)),
    _btn;

    for (let i = 0; i < _agreements.length; i++) {
        _btn = document.createElement("button");
        _btn.classList.add("tablinks");
        _btn.onclick = tabOnclick;
        _btn.innerHTML = _agreements[i].replaceAll("_","");
		_btn.value = i;
        tab_parent.appendChild(_btn);
    }

}
function tabOnclick() {
    let _t = this.value,
	     rep_type=report_state[0];	
		 process_state(rep_type,_t);		 
	set_active_panel(tab_panel2,this.textContent);
	report_state[1]=_t;
    return false;
}

function change_report(evt,report_type) {
    let rep_state=report_state[1];

	     process_state(report_type,rep_state);
		set_active_panel(tab_panel1,report_type);
		report_state[0]=report_type;
}

function process_state(report_type,rep_state)
{
		if (report_type=="Assets"){
	 process_htable(assets_data[rep_state], gradient_cols = [2]);
	}
	else if (report_type=="Sector"){
		process_htable(sectors_data[1][rep_state], gradient_cols = [1]);
		
	}
	else {
	process_htable(sectors_data[0][rep_state], gradient_cols = [1]);	
		
	};
}


function function_export_csv_() {
	    hot2.getPlugin("exportFile").downloadFile("csv", {
        filename: "table export",
        columnDelimiter: ';',
        columnHeaders: true

    });
};

function groupby_sum(matrix, group_col_id, agg_col_id) {
    let result = matrix.reduce(function (res, value) {
        if (!res[value[group_col_id]]) {
            res[value[group_col_id]] = 0;
        }
        res[value[group_col_id]] += value[agg_col_id];
        return res;
    }, {});
    return result;
}

main();







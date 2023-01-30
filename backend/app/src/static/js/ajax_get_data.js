function get_data_to_js(url,data={}) {

$.ajax({
                type: "POST",
                url: url,
                data: JSON.stringify(data),
				contentType:"application/json; charset=UTF-8",
			    
                type: 'POST',
				async: false,
                success: function(response) {
		
                     data1 = JSON.parse(response)  ;                
                },
                error: function(error) {
                    console.log(error);
                }
            });
return data1
}
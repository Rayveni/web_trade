async function get_js_data(url) {
    try {
        let resp = await fetch(url);
         const res=await resp.json();
		return res;
    } catch (error) {
        console.log(error);
    }
}


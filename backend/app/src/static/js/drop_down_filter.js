
function dropdown_filter_function(dropdown_id,dropdown_input_id) {
  var input, filter, ul, li, a, i;
  input = document.getElementById(dropdown_input_id);
  filter = input.value.toUpperCase();
  div = document.getElementById(dropdown_id);
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function dropdown_show(dropdown_id) {
  document.getElementById(dropdown_id).classList.toggle("show");
}
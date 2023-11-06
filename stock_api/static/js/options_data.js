  // Turns our table into a DataTable
  // $(document).ready(function () {
  //   $('#historical-data-table').DataTable();
  // });


// Grabs all the Rows that are part of the class 'itm-True', then add a style class to highlight that table row  
var itmRows = document.getElementsByClassName('itm-True')

for (var i = 0; i < itmRows.length; i++){
  itmRows[i].classList.add("table-primary")
}
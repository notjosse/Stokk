  // Turns our table into a DataTable
  $(document).ready(function () {
    $('#historical-data-table').DataTable();
  });

const ctx = document.getElementById('myChart');

// Convert data from a string to a usable array that can traversed
let stock_data = document.getElementById("export-json")

let data = stock_data["value"]
let sliced_data = data.slice(1,data.length -1)

let left, right = null
data_arr = []

for (let i = 0; i < sliced_data.length; i++){
    if (sliced_data[i] == "["){
        left = i
    }
    else if (sliced_data[i] == "]"){
        right = i
    }

    if (left && right){
        data_substring = sliced_data.slice(left+1, right)
        temp_arr = data_substring.split(",")
        data_arr.push(temp_arr)
        left, right = null
    }

}

// extract data from our array to put into our chart
let chart_labels = []
let chart_values = []

for (let i = data_arr.length-1; i >= 0; i--){
    chart_labels.push(data_arr[i][0])
    chart_values.push(data_arr[i][4])
}

// Build Line Chart
new Chart(ctx, {
    type: 'line',
    data: {
      labels: chart_labels,
      datasets: [{
        label: 'Close Price',
        data: chart_values,
        fill: true,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
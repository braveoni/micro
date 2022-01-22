var ctx = document.getElementById('line');

var line = new Chart(ctx, {
	type: 'line',
	data: {
		labels: [],
		datasets: [{
			label: 'Counts',
			data: [],
			backgroundColor: 'rgb(112, 68, 255, 0.3)',
			fill: true,
			tension: 0.4,
		}]
	},
	options: {
		responsive: true,
		title: {
			display: true,
			text: "Count",
		},
		plugins: {
			legend: {
				position: null,
			}
		}
	}
});

var getData = () => {
	$.ajax({
		url: '/data',
		success: function (data) {
			line.data.labels = data['line']['labels'];
			line.data.datasets[0].data = data['line']['data']

			line.update();
		}
	});
};

setInterval(getData, 500);
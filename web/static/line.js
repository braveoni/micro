var ctx = document.getElementById('line');

var line = new Chart(ctx, {
	type: 'line',
	data: {
		labels: [],
		datasets: []
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

const objectsEqual = (o1, o2) =>
	typeof o1 === 'object' && Object.keys(o1).length > 0
		? Object.keys(o1).length === Object.keys(o2).length
		&& Object.keys(o1).every(p => objectsEqual(o1[p], o2[p]))
		: o1 === o2;

var getData = () => {
	$.ajax({
		url: '/data',
		success: function (data) {
			console.log(data['line']['data']);
			if (!objectsEqual(line.data.datasets), data['line']['data']) {
				line.data.datasets = data['line']['data'];
				line.data.labels = data['line']['labels'];
				line.update();
			};
		}
	});
};

setInterval(getData, 100)
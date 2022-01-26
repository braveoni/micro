var ctx = document.getElementById('doughnut');

const randomNum = () => Math.floor(Math.random() * (235 - 52 + 1) + 52);
const randomRGB = () => `rgb(${randomNum()}, ${randomNum()}, ${randomNum()}, 0.6)`;

const objectsEqual = (o1, o2) =>
    typeof o1 === 'object' && Object.keys(o1).length > 0
        ? Object.keys(o1).length === Object.keys(o2).length
        && Object.keys(o1).every(p => objectsEqual(o1[p], o2[p]))
        : o1 === o2;

const addColor = (f, s) => {
    for (var i = 0; i < f - s; i++) {
        doughnut.data.datasets[0].backgroundColor.push(randomRGB());
    }
};

var doughnut = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: [],
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
                position: 'left',
            }
        }
    }
});

var getData = function () {
    $.ajax({
        url: '/data',
        success: function (data) {
            doughnut.data.labels = data['doughnut']['labels'];
            if (!objectsEqual(doughnut.data.datasets[0].data, data['doughnut']['data'])) {
                doughnut.data.datasets[0].data = data['doughnut']['data'];
                addColor(
                    doughnut.data.datasets[0].data.length,
                    doughnut.data.datasets[0].backgroundColor.length);
                doughnut.update();
            };
        }
    });
};

setInterval(getData, 100);
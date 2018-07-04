class BlocksPerHourChart extends React.Component {
    ref = (element) => {
        this.element = element;
    }

    componentDidMount() {
        var myChart = new Chart(this.element, {
            type: 'bar',
            data: {
                labels: this.props.day.data.map(d => d.label),
                datasets: [{
                    label: '# of Blocks',
                    data: this.props.day.data.map(d => d.bph),
                    backgroundColor: 
                       'rgba(42, 161, 152, 0.4)'
                    ,
                    borderColor: 
                        'rgba(42, 161, 152, 1)'
                    ,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Hour'
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        });
    }
    //<div id="loader" class="loader"></div>
    render() {
        return (
            <div class="chart-container">
                <h3>July {this.props.day.num} - {this.props.day.total} Blocks</h3>
                <canvas ref={this.ref}></canvas>
            </div>
        )
    }
}

class BlocksPerHourContainer extends React.Component {
    constructor() {
        super()
        this.state = {
            days: []
        }
    }
    componentDidMount() {
        fetch('/api/stats/blocksPerHour')
        .then(response => {
            return response.json();
        })
        .then(myJson => {
            Object.keys(myJson).forEach((day) => {
                var data = []
                var total = 0
                Object.keys(myJson[day]).forEach((key) => {
                    data.push({label: key, bph: myJson[day][key]})
                    total += myJson[day][key]
                });
                data.sort((a,b) => a.label - b.label)
                this.setState((prev, next) => prev.days.push({num: day, data: data, total: total}))
            })
        });
    }

    render() {
        return (
            <div id="stats">
                <div class="row">
                {this.state.days.length === 0 ?
                        <div id="loader" class="loader"></div> :
                        this.state.days.map(day => {
                            return (
                                <div class="col-lg-6">
                                    <BlocksPerHourChart day={day} />
                                </div>
                            )
                        })
                    }
                </div>
            </div>
        )
    }
}
  
  const rootElement = document.getElementById('root')
  function App() {
    return(
    <div class="container-fluid">
        <h2 class="mb-4">Blocks Mined</h2>
        <BlocksPerHourContainer />
    </div>
    )
  }
  
  ReactDOM.render(
    <App />,
    rootElement
  )
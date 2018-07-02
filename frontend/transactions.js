class Transaction extends React.Component {
  render() {
    return (
      <div class="col-md-6 col-12">
       <div class="card block">
        <div class="card-body">
          <p class="text-center transaction">
            <div class="hash">{this.props.transaction.sender}</div>
            <div class="text-info arrow">⇓ ¢{this.props.transaction.amount}</div>
            <div class="hash">{this.props.transaction.reciever}</div>
            {/* <div class="hash">{this.props.transaction.signature}</div> */}
          </p>
        </div>
       </div>
      </div>
    )
  }
}
// Create a ES6 class component   
class TransactionList extends React.Component { 
  constructor() {
    super()
    this.state = {
      transactions: [],
      loading: false
    }
  }
  componentDidMount() {
    this.setState({loading: true})
    fetch('/api/transactions')
      .then(response => {
        return response.json();
      })
      .then(myJson => {
        this.setState((prevState, props) => {
          return {transactions: myJson, loading: false};
        });
    });
  }
// Use the render function to return JSX component      
render() { 
    return (
    <div class="row">
      {this.state.loading ? 
      <div class="loader"></div> :
      this.state.transactions == 0 ?
      <div class="col-12 text-center mt-4"><h2>There are no pending transactions.</h2></div> :
      this.state.transactions.reverse().map(transaction=> <Transaction transaction={transaction}></Transaction>)}
    </div>
  );
  } 
}

const rootElement = document.getElementById('root')
function App() {
  return(
  <div class="container-fluid">
    <TransactionList />
  </div>
  )
}

ReactDOM.render(
  <App />,
  rootElement
)
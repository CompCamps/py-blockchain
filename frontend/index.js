class Transaction extends React.Component {
  render() {
    return (
      <p class="text-center transaction">
        <div class="hash">{this.props.transaction.sender}</div>
        <div class="text-info arrow">⇓ ¢{this.props.transaction.amount}</div>
        <div class="hash">{this.props.transaction.reciever}</div>
      </p>
      
    )
  }
}

class Block extends React.Component {
  render() {
    return (
      <div class="col-lg-6 col-12">
        <div class="card block">
          <div class="card-header">
            <h5 class="card-title">Block #: {this.props.block.index} <span class="right text-small">{this.props.block.timestamp}</span></h5>
            Nonce: <span class="hash">{this.props.block.nonce}</span><br/>
            Hash: <span class="hash">{this.props.block.hash}</span>
          </div>
          <div class="card-body transactions">
            {this.props.transactions.map(transaction => <Transaction transaction={transaction}></Transaction>)}
          </div>
          <div class="card-footer">
            Previous Hash: <span class="hash">{this.props.block.previousHash}</span>
          </div>
        </div>
      </div>
    )
  }
}
// Create a ES6 class component   
class BlockChain extends React.Component { 
  constructor() {
    super()
    this.state = {
      blocks: []
    }
  }
  componentDidMount() {
    fetch('/api/chain')
      .then(response => {
        return response.json();
      })
      .then(myJson => {
        this.setState((prevState, props) => {
          return {blocks: myJson};
        });
    });
  }
// Use the render function to return JSX component      
render() { 
    return (
    <div class="row">
      {this.state.blocks.length == 0 ? 
      <div class="loader"></div> :
      this.state.blocks.reverse().map(block=> <Block block={block} transactions={JSON.parse(block.transactions)}></Block>)}
    </div>
  );
  } 
}

const rootElement = document.getElementById('root')
function App() {
  return(
  <div class="container-fluid">
    <BlockChain />
  </div>
  )
}

ReactDOM.render(
  <App />,
  rootElement
)
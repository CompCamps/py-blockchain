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
      blockGroups: [],
      show: 0,
      chunkCount: 0
    }
  }
  componentDidMount() {
    fetch('/api/chain')
      .then(response => {
        return response.json();
      })
      .then(myJson => {
        this.setState((prevState, props) => {
          var chunkCount = Math.round(myJson.length/500);
          var chunkSize = Math.round(myJson.length/chunkCount/500) * 500;
          myJson = myJson.reverse()
          var groups = myJson.map( function(e,i){ 
              return i%chunkSize===0 ? myJson.slice(i,i+chunkSize) : null; 
          }).filter(function(e){ return e; });
          return {blockGroups: groups, chunkCount: chunkCount};
        });
    });
  }

  showMore() {
    this.setState({show: this.state.show + 1})
  }
// Use the render function to return JSX component      
render() { 
    return (
    <div class="row">
      {this.state.blockGroups.length == 0 ? 
      <div class="loader"></div> :
      this.state.blockGroups.map((group, index) =>
        index <= this.state.show ? group.map(block=> <Block block={block} transactions={JSON.parse(block.transactions)}></Block>) : ''
      )}
      {this.state.blockGroups.length > 0 && this.state.show < this.state.chunkCount-1 ? 
      <div class="col-12 text-center mb-3">
        <button class="btn btn-link" onClick={this.showMore.bind(this)}>Show More</button>
      </div> : ''}
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
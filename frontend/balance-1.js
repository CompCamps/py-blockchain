class BalanceList extends React.Component {
  constructor() {
    super()
    this.state = {
      balances: [],
      loading: false
    }
  }

  sort(a, b) {
    return a.balance - b.balance;
  }

  componentDidMount() {
    this.setState({loading: true});
    fetch('/api/balances')
    .then(response => {
      return response.json();
    })
    .then(myJson => {
      this.setState((prevState, props) => {
        var balances = []
        Object.keys(myJson).forEach(function (key, value) {
          balances.push({key: key, balance: myJson[key]})
        });
        return {balances: balances.sort(this.sort).reverse(), loading: false};
      });
    });
  }

  render() {
    return (
      <div class="row">
        {this.state.loading ? 
          <div class="loader"></div> :
          <ul class="list-group col-8 offset-2">
          {this.state.balances.map(function(bal) {  
            return (<li class="list-group-item"><span class="hash">{bal.key}</span> <span class="balance right text-info">¢{Math.round(bal.balance * 1000)/1000}</span></li>)
          })}
          </ul>
        }
      </div>
      
    )
  }
}
class Balance extends React.Component { 
  constructor() {
    super()
    this.state = {
      balance: '',
      publicKey: '',
      loading: false
    }
  }
  handleChange(event) {
    this.setState({publicKey: event.target.value});
  }
  encodeURL(str){
    return str.replace(/\+/g, '-').replace(/\//g, '_').replace(/\=+$/, '');
  }
  onSubmit() {
    if (this.state.publicKey.length === 0) return
    fetch('/api/balance?public_key=' + encodeURIComponent(this.state.publicKey))
    .then(response => {
      return response.json();
    })
    .then(myJson => {
      this.setState((prevState, props) => {
        return {balance: myJson, loading: false};
      });
    });
  }
  onBalanceImage(e) {
    if (this.state.publicKey.length === 0) return
    window.location.href = '/api/balance?image=true&public_key=' + encodeURIComponent(this.state.publicKey)
    e.preventDefault();
  }
// Use the render function to return JSX component      
render() { 
    return (
    <div class="row">
      {this.state.loading ? 
      <div class="loader"></div> : ''}
      <form class="col-8 offset-2">
        <div class="form-group">
          <label for="publicKey">Public Key</label>
          <input class="form-control" id="publicKey" type="text" value={this.state.publicKey} onChange={this.handleChange.bind(this)} placeholder="Enter a public key" required/>
        </div>
        <div class="form-group">
        <button class="w-25 btn btn-info right" onClick={this.onSubmit.bind(this)}>Get Balance</button>
        <button class="w-25 btn btn-secondary right mr-2" onClick={this.onBalanceImage.bind(this)} type="submit">Generate Image</button>
        </div>
      </form>
      
      <div class="col-8 offset-2">
      <h3>Balance: {this.state.balance}</h3>
      <hr class="mb-4"/>
      <div class="text-center">
        <h4>All Wallets</h4>
      </div>
      </div>
    </div>
  );
  } 
}

const rootElement = document.getElementById('root')
function App() {
  return(
  <div class="container-fluid">
    <Balance />
    <BalanceList />
  </div>
  )
}

ReactDOM.render(
  <App />,
  rootElement
)
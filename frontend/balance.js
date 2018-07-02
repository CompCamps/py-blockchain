// Create a ES6 class component   
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
  onSubmit() {
    //this.setState({loading: true});
    fetch('https://campcoin.herokuapp.com/api/balance', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: 'post',
      body: JSON.stringify({"public_key": this.state.publicKey})
    }).then(response => {
      return response.json();
    })
    .then(myJson => {
      console.log(myJson)
      this.setState((prevState, props) => {
        return {balance: myJson, loading: false};
      });
    });
  }
// Use the render function to return JSX component      
render() { 
    return (
    <div class="row">
      {this.state.loading ? 
      <div class="loader"></div> : ''}
      <div class="col-6 offset-3">
        <div class="form-group">
          <label for="publicKey">Public Key</label>
          <input class="form-control" id="publicKey" type="text" value={this.state.publicKey} onChange={this.handleChange.bind(this)}/>
        </div>
        <div class="form-group">
        <button class="w-50 btn btn-info right" onClick={this.onSubmit.bind(this)}>Submit</button>
        </div>
      </div>
      
      <div class="col-6 offset-3">
      <hr/>
      <h3>Balance: {this.state.balance}</h3>
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
  </div>
  )
}

ReactDOM.render(
  <App />,
  rootElement
)
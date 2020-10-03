import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {BrowserRouter, Route} from 'react-router-dom'
import {Provider} from 'react-redux'
import {createStore, applyMiddleware} from 'redux'
import reducer from './reducers/'
import reducers from './reducers'
import thunk from 'redux-thunk'
import {logger} from 'redux-logger'



const store = createStore(reducers, applyMiddleware(thunk,logger))

ReactDOM.render(
  // <React.StrictMode>
  <BrowserRouter>
  <Provider store={store}>
    <Route path='/' render = {(navigation)=>{return <App navigation={navigation} />}}/>

  </Provider>
  </BrowserRouter>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

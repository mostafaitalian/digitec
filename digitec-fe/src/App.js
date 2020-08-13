import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import LogRocket from 'logrocket'
import axios from 'axios'
import Nav from './components/Nav'
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'redux'
import LoginForm from './components/LoginForm'
import SignUpForm from './components/SignUpForm'



LogRocket.init('mvwrjh/digitec1')
const config = {
  headers: {
    'Content-Type': 'application/json',
    // 'X-CSRFToken': csrftoken,
  }
}


class App extends Component {

  state = {
    username: '',
    loggedIn: false,
    users:[]

  }
  handleLogin = (e, data) => {
    e.preventDefault()
    fetch('http://127.0.0.1:8000/token-auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(res => res.json())
      .then(dataa => {
        console.log('dataa', dataa)
        localStorage.setItem('token', JSON.stringify(dataa))
        console.log('local storage token ', localStorage.getItem('token'))
        this.setState({
          loggedIn: true,
          username: dataa.user.username
        })




      })
  }
  handleSignUp = (e, data) => {
    fetch('http://127.0.0.1:8000/users/api/userss/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
     
      body: JSON.stringify(data)
    }).then(
      res => res.json()
    ).then(
      data => {
        console.log('sign up data', data)
      }
    )
  }

  handleLogOut = e => {
    e.preventDefault()
    localStorage.removeItem('token')
    this.setState({
      username: '',
      loggedIn: false,
    })
  }

  componentDidMount() {
    if (this.state.loggedIn) {

      fetch('http://127.0.0.1:8000/users/api/current-user/', {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`
        }
      })
        .then(
          res => res.json()
        ).then(data => {
          console.log('data from current-user url in app did mount', data)
          this.setState({
            username: data.username
          })
        }).catch(errors => console.warn(errors))
    //     fetch('http://127.0.0.1:8000/users/api/user-list/',{
    //       method:'GET',
    //       headers:{
    //         'Content-Type':'application/json'
    //       }

    //     })
    //     .then(
    //       res=>res.json()
    //     ).then(
    //       data=>{
    //         console.log('data from user-list in app did mount', data)
    //         this.setState({users: data})
    //       }
    //     )
    // }
      }
  }
  render() {
    console.log('username', this.state.username.length)
    let userName = (this.state.username.length === 0) ? 'for you' : this.state.username
    return (
      <BrowserRouter>
        <div className='container-fluid'>
          <Nav userName={userName} loggedIn={this.state.loggedIn} handleLogOut={this.handleLogOut} />
          <LoginForm handleLogin={this.handleLogin} />
          <SignUpForm handleSignUp={this.handleSignUp}></SignUpForm>

          {
            JSON.stringify(this.state.users)
          }
        </div>
      </BrowserRouter>


    )
  }

}

export default App;

import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import LogRocket from 'logrocket'
import axios from 'axios'
import Nav from './components/Nav'
import { BrowserRouter, Route,Link } from 'react-router-dom'
import { Provider } from 'redux'
import LoginForm from './components/LoginForm'
import SignUpForm from './components/SignUpForm'
import MachineList from './components/MachineList';
import {useHistory} from 'react-router-dom'
import {connect} from 'react-redux'
import {addLoggedInUser, deleteLoggedInUser} from './actions/authorizeUser'
import UserSummary from './components/UserSummary'
import LikeButton from './components/Likebutton'

export const baseUrl = "http://178.79.144.93:8000/"

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
    fetch(`${baseUrl}token-auth/`, {
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
        this.props.dispatch(addLoggedInUser(dataa.user))







        console.log('prooooooooooooooops', this.props)
        this.props.navigation.location['pathname']='/'
        this.props.navigation.history.replace('machines/')
      })
  }
  handleSignUp = (e, data) => {
    fetch(`${baseUrl}users/api/user-list/`, {
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
    this.props.navigation.location['pathname']='/'
    this.props.navigation.history.replace('login/')
  }

  handleLogOut = e => {
    e.preventDefault()
    localStorage.removeItem('token')
    this.setState({
      username: '',
      loggedIn: false,
    })
    this.props.dispatch(deleteLoggedInUser())
    console.log('prooooooooooooooops', this.history,this.props)
    this.props.navigation.location['pathname']='/'
    this.props.navigation.history.push('login/')
    // this.props.history.goBack()
    // this.props.history.replace('login/')
  }

  componentDidMount() {
    let token =  ''
    let user = {}
    if(localStorage.getItem('token')){
      console.log('local storage',(localStorage.getItem('token'))['token'])
      const data = JSON.parse(localStorage.getItem('token'))
      token = data['token']
      user = data.user?data.user:{}
      console.log('token', token)
      console.log('navigation from app', this.props)
    }

      fetch(`${baseUrl}users/api/current-user/`, {
        headers: {
          Authorization: `JWT ${token}`
        }
      })
        .then(
          res => res.json()
        ).then(data => {
          console.log('data from current-user url in app did mount', data)
          this.setState({
            loggedIn:true,
            username: data.user.username
          })
          this.props.dispatch(addLoggedInUser(data.user))
        }).catch(errors => {
          console.warn(errors)
          this.setState({

          })
        })
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
  
  render() {
    console.log('username', this.state.username.length)
    let userName = (this.state.username.length === 0) ? 'for you' : this.state.username
    return (
        <div className='container-fluid'>
        {/* {JSON.stringify(this.props)} */}

          <Route path='/' render={(navigation)=><Nav userName={userName} loggedIn={this.state.loggedIn} loggedInUser={this.props.state.loggedInUser} handleLogOut={this.handleLogOut} navigation={navigation} />} />
          <Route exact path='/machines' render={(navigation)=>{
          console.log('navigation', navigation)
          return <MachineList navigation={navigation}/>}}/>
          <Route path='/login' render={(navigation)=>{
          return <LoginForm navigation={navigation} handleLogin={this.handleLogin} />}} />

          <Route exact path='/user/:id' render={(navigation)=>{
          return <UserSummary navigation={navigation}/>}} />     
          
          <Route path='/signup' render={(navigation)=>{
            console.log(navigation)
          return <SignUpForm navigation={navigation} handleSignUp={this.handleSignUp} />}} />
          {
            JSON.stringify(this.state.users)
          }


          <LikeButton/>
        </div>
    


    )
  }

}

export default connect(state=>{return {state:state}})(App)

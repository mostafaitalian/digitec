import React, { Component } from 'react'
import PropTypes from 'prop-types'


class LoginForm extends Component {

    state = {
        username: '',
        password: '',
    }
    handleOnChange = e =>{
        const name = e.target.name
        const value = e.target.value
        this.setState((prev)=>{
            return {
                ...prev, [name]:value
            }
        })

    }

    handleOnSubmit = (e)=>{
        e.preventDefault()
        this.props.handleLogin(e,this.state)
        this.setState({
            username:'',
            password:''
        })
    }
    render() {
        return (
            <div>
                <h1> Login here</h1>
                <form onSubmit={e=>this.handleOnSubmit(e)}>
                    <div className='form-group'>
                        <label htmlFor='username'>
                            Username
                        </label>
                        <div className='form-control'>
                            <input 
                            type='text' 
                            name='username' 
                            placeholder='enter your username here' 
                            value={this.state.username}
                            onChange={this.handleOnChange}
                            />
                        </div>

                    </div>
                    <div className='form-group'>
                        <label htmlFor='password'>
                            Password
                        </label>
                        <div className='form-control'>
                            <input 
                            type='password' 
                            name='password' 
                            placeholder='enter your password here' 
                            value={this.state.password}
                            onChange={this.handleOnChange}
                            />
                        </div>

                    </div>
                    <button type='submit'>Login</button>
                </form>
            </div>
        )
    }




}


export default LoginForm



LoginForm.propTypes = {}
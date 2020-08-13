import React, { Component } from 'react'
import PropTypes from 'prop-types'


class SignUpForm extends Component {

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
        this.props.handleSignUp(e,this.state)
        this.setState({
            username:'',
            password:''
        })
    }

    render() {
        return (
            <div>
                <h1> signup here</h1>
                <form onSubmit={this.handleOnSubmit}>
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
                            type='text' 
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


export default SignUpForm



SignUpForm.propTypes = {}
import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'



class UserSummary extends Component {


    render() {
        const loggedInUser = this.props.state['loggedInUser']
        console.log('loggedInUser', this.props.state, this.props)

        return (
            <div>
                {/* User summary */}
                {/* {JSON.stringify(this.props.state['loggedInUser'])} */}
                {(loggedInUser && loggedInUser.engineer) ? <h3>Welcome Engineer {loggedInUser['username']}-{loggedInUser.engineer.name}</h3> : ''}
                {(loggedInUser && loggedInUser.is_superuser) ? <h3>Welcome Admin {loggedInUser['username']}</h3> : ''}
                {
                    this.props.navigation.match.url === '/user/undefined' ?
                        (<div className='card mt-3 '>
                            <div className='card-body shadow-sm' style={{fontFamily: 'Palatino Linotype'}}>
                                You are not authorized to see this page
                                    <br/><br/>
                                You may need to <span className="bg-primary text-white p-1">login</span> or <span className='bg-success text-white p-1'>register</span>
                            </div>
                            <div className='text-center'>
                                 
                            <Link className='btn btn-primary text-center m-3' to='/login' >Login</Link>
                                <Link className='btn btn-success text-center m-3' to='/signup' >SignUp</Link>
                            </div>
                            

                            </div>
                            ):''
                }
                        </div>
                        )
    }
}
function mapStateToProps(state, ownProps){

    return {
                    loggedInUser: state.loggedInUser
    }
}
export default connect(state=> {return {state:state}})(UserSummary)
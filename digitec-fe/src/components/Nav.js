import React, { Component, Fragment } from 'react'
import { Link } from 'react-router-dom'



class Nav extends Component {

  render() {
    const { userName, loggedIn } = this.props
    console.log('nav props', this.props)
    return (
      <nav className="navbar navbar-expand-md navbar-light">
        <button className="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <a className="navbar-brand" href="http://localhost:8000/">Digitec</a>

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            <li className='nav-item active'>
              <a className='nav-link' href=''>Home <span className='sr-only'>(current)</span></a>
            </li>
            <li className='nav-item'>
              <a className='nav-link' href=''>About</a>
            </li>
            <li className='nav-item text-center'>
              <a className='nav-link text-center' href='contactus'>Contact us</a>
            </li>
            {
              this.props.loggedIn ?
                <Fragment>
                  <li className='nav-item text-center'>
                    {/* <a className='nav-link text-center' href='machines'>Machine list</a> */}
                    <Link to='/machines' className='nav-link text-center'>
                      Machine List
                    </Link>
                  </li>
                  <li className='nav-item text-center'>
                    <a className='nav-link text-center' onClick={this.props.handleLogOut} href=''>Logout</a>
                  </li>
                </Fragment>
                :
                <Fragment>
                  <li className='nav-item text-center ' style={{ textDecorationLine: 'none' }}>
                    <Link className='nav-link text-center' to='/signup' >Signup</Link>
                  </li>
                  <li className='nav-item text-center'>
                    <Link className='nav-link text-center' to='/login' >login</Link>
                  </li>
                </Fragment>


            }


            <li className='nav-item'>
              <Link to={this.props.loggedInUser?`/user/${this.props.loggedInUser.id}`:''} className='nav-link' href=''>welcome {userName}</Link>
            </li>

          </ul>
        </div>
      </nav>
    )
  }


}
export default Nav
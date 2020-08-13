import React, { Component, Fragment } from 'react'



class Nav extends Component {

  render() {
    const userName = this.props.userName
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
              <a className='nav-link text-center' href=''>Machine-list</a>
            </li>
            {
              this.props.loggedIn ?
                <li className='nav-item text-center'>
                  <a className='nav-link text-center' onClick={this.props.handleLogOut} href=''>Logout</a>
                </li> :
                <Fragment>
                  <li className='nav-item text-center ' style={{ textDecorationLine: 'none' }}>
                    <a className='nav-link text-center' href=''>Signup</a>
                  </li>
                  <li className='nav-item text-center'>
                    <a className='nav-link text-center' href=''>Login</a>
                  </li>
                </Fragment>


            }


            <li className='nav-item'>
              <a className='nav-link' href=''>welcome {userName}</a>
            </li>

          </ul>
        </div>
      </nav>
    )
  }


}
export default Nav
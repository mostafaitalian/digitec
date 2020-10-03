import React, {Component} from 'react'
import {connect} from 'react-redux'
import {Tabs,Tab,Container, Row, Col} from 'react-bootstrap'


class CallList extends Component{
    render(){
        
        return(
            <div>
                <Container>
                <Row><Col>
                    {/* <nav>
                        <Tabs  style={{display:'flex', justifyContent:'space-around'}}>
                            <Tab className='tabo' eventKey='home' title='home' style={{width:'20px'}}></Tab>
                            <Tab className='tabo' eventKey='about' title='about'></Tab>
                            <Tab className='tabo' eventKey='about' title='about'></Tab>
                            <Tab className='tabo' eventKey='about' title='about'></Tab>
                            <Tab className='tabo' eventKey='about' title='about'></Tab>

                        </Tabs>
                    </nav> */}
                    </Col>
                </Row>
                    <Row style={{marginTop:'25px'}}>
                        <Col>

                        </Col>
                        <Col className='lead' lg={8} md={8} sm={10} xs={12}>
                            <Tabs className='navbar navbar-default'  id='controlled-tab' style={{display:'flex'}}>
                                
                                <Tab eventKey='unanswered' title='unanswered' style={{width:'100%', flex:'0.5'}}>
                                <div  style={{marginTop:'25px',border:'1px solid black'}}>
                                <p>
./src/components/SignUpForm.js
  Line 2:8:  'PropTypes' is defined but never used  no-unused-vars

./src/components/CallList.js
  Line 2:9:  'connect' is defined but never used  no-unused-vars

./src/components/UserSummary.js
  Line 42:10:  'mapStateToProps' is defined but never used  no-unused-vars

./src/components/MachineList.js
  Line 5:9:    'ADD_MACHINES' is defined but never used       no-unused-vars
  Line 6:30:   'Card' is defined but never used               no-unused-vars
  Line 6:36:   'Button' is defined but never used             no-unused-vars
  Line 57:16:  'machines' is assigned a value but never used  no-unused-vars

./src/reducers/authorizeUser.js
  Line 9:13:  Unreachable code  no-unreachable

./src/components/Nav.js
  Line 9:23:   'loggedIn' is assigned a value but never used</p>
                                {/* {unansweredArray.length===0&&<h2>you answered all question in the game</h2>}

                                {
                                    unansweredArray.sort((a,b)=>b.timestamp-a.timestamp).map((qid)=>{
                                       return <Question key={qid.id} id={qid.id}/>
                                    })
                                } */}
                                </div>
                                </Tab>
                                <Tab eventKey='answered' title='answered' style={{width:'100%', flex:'0.5', }}>
                                <div style={{marginTop:'25px', border:'1px solid black'}}>
                                {/* {answeredArray.length===0&&<h4>you didnot answer any question yet</h4>}
                                {
                                    answeredArray.sort((a,b)=>b.timestamp-a.timestamp).map((qid)=>{
                                       return <Question key={qid.id} id={qid.id}/>
                                    })
                                } */}
                                <p>
                                Line 39:21:  The href attribute requires a valid value to be accessible. Provide a valid, navigable address as the href value. If you cannot provide a valid href, but still need the element to resemble a link, use a button and change it with appropriate styles. Learn more: https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/anchor-is-valid.md  jsx-a11y/anchor-is-valid
                                </p>
                                </div>
                                </Tab>
                            </Tabs>
                        </Col>
                        <Col>

                        </Col>
                    </Row>
                </Container>
            </div>
        )
    }
}

export default CallList
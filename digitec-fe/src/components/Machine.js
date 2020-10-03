import React, { Component } from 'react'
import { Container, Row, Col, Accordion, Card, Button } from 'react-bootstrap'
import Review from './Review'

class Machine extends Component {


    render() {
        const { ind, machine } = this.props
        console.log('key and machine', ind, machine)
        return(

                <Card id={`${this.props.machine.serial}`}>
                    <div style={{display:'flex', flexDirection:'row',flexWrap:'wrap'}}>

                    </div>
                    <Card.Header style={{backgroundColor:'gray', color:'white', textDecoration:'none'}}>
                        <Accordion.Toggle as={Button} variant="link" eventKey={`${this.props.ind}`}
                        style={{color:'white', textDecoration:'none'}}
                        >
                            Click me!-{this.props.machine.name}-{this.props.machine.serial}
                        </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey={`${this.props.ind}`}>
                        <Card.Body>
                        <Card.Text style={{fontSize:26}}>
                           Customer Name: {this.props.machine.customer.name}                        
                        </Card.Text>
                        <Card.Text>
                            {this.props.machine.speed}

                        </Card.Text>
                        
                        <Card.Title style={{color:'white',backgroundColor:'blue', textDecoration:'none'}}>
                            All reviews for {this.props.machine.name}-{this.props.machine.serial}
                        </Card.Title>
                        <Accordion defaultActiveKey='0'>
                        {
                             this.props.machine.reviews.length>0?
                             this.props.machine.reviews.map((review, i)=>{
                               return <Review key={i} ind={i} review={review}/>
                             }):<Card.Text>no reviews for this machine yet</Card.Text>
                         }
                        </Accordion>
                         
                         </Card.Body>
                    </Accordion.Collapse>
                </Card>

        )
    }
}


export default Machine
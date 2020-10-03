import React, { Component, Fragment } from 'react'
import { Container, Row, Col, Accordion, Card, Button, Carousel } from 'react-bootstrap'


class Review extends Component {


    render() {


        return (

            <Card>
                <Card.Header>
                    <Accordion.Toggle as={Button} variant="link" eventKey={`${this.props.ind}`}>
                        Click me!-{this.props.review.review_title}
                    </Accordion.Toggle>
                </Card.Header>
                <Accordion.Collapse eventKey={`${this.props.ind}`}>
                    <Card.Body>
                        <Card.Text>
                            Suggestion: {this.props.review.review_content}
                        </Card.Text>
                        <Card.Text>
                            creation date: {this.props.review.created_at}

                        </Card.Text>

                        <Card.Img variant="bottom" src={this.props.review.image} />
                        {
                            this.props.review.file_data ? <a href={`${this.props.review.file_data}`} download color='red'>
                               <Card.Text style={{backgroundColor:'gray'}}>
                               you can also download that file too
                               </Card.Text>
                            <Card.Img variant="bottom" src={this.props.review.file_data} />

                            </a> : ''


                        }






                        <Carousel>
                            {
                                this.props.review.images.map((im, i) => {
                                    return (
                                        <Carousel.Item>
                                            <img
                                                className="d-block w-100"
                                                src={im.image}
                                                alt={`slide ${i}`}
                                            />
                                            <Carousel.Caption>
                                                <h3>{im.image_name}</h3>
                                                <p>{im.image_description}</p>
                                            </Carousel.Caption>
                                        </Carousel.Item>
                                    )

                                
                                })
                            }
                             

                                   </Carousel>

                                









                                        
























                    </Card.Body>
                </Accordion.Collapse>
            </Card>

        )
    }
}


export default Review
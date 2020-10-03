import React,{Component} from 'react'
import axios from 'axios'
import {baseUrl} from '../App'
import {connect} from 'react-redux'
import {ADD_MACHINES, addMachines} from '../actions/machines'
import {Container, Row, Col, Card, Button, Accordion} from 'react-bootstrap'
import Machine from './Machine'
import Board from './Board'
import CallList from './CallList'

class MachineList extends Component{


    state = {
        machines:[],
      }
      componentDidMount(){
        const token = JSON.parse(localStorage.getItem('token'))?JSON.parse(localStorage.getItem('token'))['token']:''
        // axios.post(`${baseUrl}token-auth/`).then(
        //   res=>console.log('token',res)
        // ).catch(errors=>console.log(errors))
        axios.get(`${baseUrl}machine/api/`, {
          headers:
          {
            'Authorization': `JWT ${token}`
          }
        })
        // .then(res=>res.json())
        .then(
          (res)=>{
            console.log('machinelist res res data', [...res.data])
            this.setState({machines: [...res.data]})
            let machinesArray = [...res.data]
            let machines = {}
            for (const machine of machinesArray){
              machines = {...machines, [machine.id]:{...machine}}
            }
            this.props.dispatch(addMachines(machines))


    
    
            // this.props.dispatch(addMachines())
          
          }
    
          ).catch(
            error=>console.warn('error-machine-list',error)
          )
          //console.log(this.state.machines)
    
        }
      
      render(){

        console.log('machine list props ', this.props)
        const {machines} = this.state
        console.log("machines", this.state.machines)
        let machinesRedux = this.props.state.machines
        const machinesKeys = Object.keys(machinesRedux)
        let machineList = []

        for(const k of machinesKeys){
          machineList.push(this.props.state.machines[`${k}`].serial)
        }
        console.log('machineRedux', machinesRedux, machineList)
        // machinesKeys.map((key, index)=>{

        // })
      return (
        
        <Container fluid>





                <Row>
                    <Col>       
</Col>
                    <Col xs={10} xm={6} xl={6}>
                    <Board serials={machineList}/>
                    <div className="App">


<Accordion defaultActiveKey="0">

{
  machinesKeys.map((keyy, index)=>{
    return <Machine key={index} ind={index} machine={machinesRedux[keyy]} />
  })
}
</Accordion>
</div>
                    </Col>
                    <Col>3 of 3</Col>
                </Row>
                <Row>
                <Col>
                <CallList/>
                </Col>
                 
                </Row>
            </Container>

      )
      }
}

export default connect(state=>{return {state:state}})(MachineList)
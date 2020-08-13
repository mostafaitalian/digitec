import React,{Component} from 'react'


class MachineList extends Component{


    state = {
        machines:[],
      }
      componentDidMount(){
        axios.post('http://127.0.0.1:8000/token-auth/').then(
          res=>console.log('token',res)
        ).catch(errors=>console.log(errors))
        axios.get('http://127.0.0.1:8000/machine/api/')
        .then(
          (res)=>{
            console.log(res, [...res.data])
            this.setState({machines: [...res.data]})}
    
          ).catch(
            error=>console.warn('error',error)
          )
          //console.log(this.state.machines)
    
        }
      
      render(){
        const {machines} = this.state
        console.log(this.state.machines)
      return (
        <div className="App">
            {
              machines.map((m,i)=>{
                return <div style={{backgroundColor:'yellow'}} key={i}>{m.serial}</div>
              })
            }
        </div>
      )
      }
}
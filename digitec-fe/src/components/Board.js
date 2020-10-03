import React, {Component} from 'react';
import classnames from 'classnames';
import {connect} from 'react-redux'

// the exported component can be either a function or a class

// export default function Board({ initialConfiguration, onSolveCallback }) {
//   return null;
// }

class Board extends Component{
    
    state = {
        initialConfiguration:[1,2,0,4,5,6,3,8,9,10,7,12,13,14,11,15]
    }
    // ref= React.createRef()
    handleOnClick = (e) =>{
        console.log('eeeeeeeeeeeee', e.target.text)
        if( e.target.value === ' '){
            // console.log('i pressed 0', this.x.innerText)
            return
        }
        else{
            let indexOfZero = this.state.initialConfiguration.indexOf(0)
            let indexOftarget = this.state.initialConfiguration.indexOf((parseInt(e.target.text)))
            // console.log(this.x,indexOfZero, indexOftarget, this.x.innerHTML, e.target.value)
            
        }
    }
    render(){
        return(
            <div className="board" style={{display:'flex', flexDirection:'row',flexWrap:'wrap',justifyContent:'space-evenly',alignItems:'center', backgroundColor:'lightgray'}}>

                {
                    this.props.serials.map((v,i)=>{
                        return <div key={i} style={{width:'32%',margin:'8px 0px',padding:'2px', textAlign:'center'}}>
                        <a href={`#${v}`} onClick={this.handleOnClick} className={v===0?'empty':'tile btn btn-outline-secondary'}
                        style={{color:'white', textDecoration:'none'}}>
                        {v !== 0?`${v}`:' '}
                        </a>
                        </div>
                    })
                }
            </div>
            )
    }
}

export default Board